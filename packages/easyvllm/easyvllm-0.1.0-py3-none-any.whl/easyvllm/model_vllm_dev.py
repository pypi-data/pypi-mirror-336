import atexit
import re
from typing import Annotated, List, Optional, Literal, Union
import concurrent.futures
import threading
import os
import subprocess
import signal
import time
from dataclasses import dataclass, replace

from openai import OpenAI, APIConnectionError
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer
from vllm.entrypoints.openai.reasoning_parsers import ReasoningParserManager, ReasoningParser

from easyvllm.parsers import *


@dataclass
class ChatParam:
    temperature: float = None
    top_p: float = None
    presence_penalty: float = None
    frequency_penalty: float = None
    max_completion_tokens: int = None

@dataclass
class ChatExtraParam:
    best_of: Optional[int] = None
    use_beam_search: bool = False
    top_k: Optional[int] = None
    min_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    length_penalty: float = 1.0
    stop_token_ids: Optional[List[int]] = None
    include_stop_str_in_output: bool = False
    ignore_eos: bool = False
    min_tokens: int = 0
    skip_special_tokens: bool = True
    spaces_between_special_tokens: bool = True
    prompt_logprobs: Optional[int] = None
    
@dataclass
class GenParam:
    temperature: float = None
    top_p: float = None
    presence_penalty: float = None
    frequency_penalty: float = None
    max_tokens: int = None

@dataclass
class GenExtraParam:
    use_beam_search: bool = False
    top_k: Optional[int] = None
    min_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    length_penalty: float = 1.0
    stop_token_ids: Optional[List[int]] = None
    include_stop_str_in_output: bool = False
    ignore_eos: bool = False
    min_tokens: int = 0
    skip_special_tokens: bool = True
    spaces_between_special_tokens: bool = True
    allowed_token_ids: Optional[List[int]] = None
    prompt_logprobs: Optional[int] = None


class InferenceModel:
    def __init__(
        self, 
        model_path: str, 
        device_ids: list[int] = None,
        tensor_parallel_size: int = 1,
        pipeline_parallel_size: int = 1,
        port: int = 50000,
        max_model_len: int = None,
        show_vllm_log: bool = True,
        openai_timeout: int = 30,
        enable_reasoning: bool = False,
        reasoning_parser: str = 'deepseek_r1',
        chat_template: str = None,
        use_ray: bool = False,
        ray_host_ip: str = None,
    ):
        
        self.model_process = []
        self.sub_pid = set()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        atexit.register(self._cleanup)

        self.tensor_parallel_size = tensor_parallel_size
        self.pipeline_parallel_size = pipeline_parallel_size
        self.model_path = model_path
        self.device_ids = device_ids or list(range(torch.cuda.device_count()))
        self.port = port
        self.max_model_len = max_model_len
        self.show_vllm_log = show_vllm_log
        self.openai_timeout = openai_timeout
        self.chat_template = chat_template
        
        self.enable_reasoning = enable_reasoning
        if enable_reasoning and not reasoning_parser:
            raise ValueError("enable_reasoning reqiures reasoning_parser")
        self.reasoning_parser = reasoning_parser
        
        self.use_ray = use_ray
        if use_ray and ray_host_ip is None:
            raise ValueError('ray_host_ip is needed when using ray')
        self.ray_host_ip = ray_host_ip
        
        self.tokenizer = None
        self.reasoning_parser_obj = None
        self.more_reasoning_prompt = 'Wait! Wait! Wait!'
        
        if use_ray:
            print('Using Ray, Only init 1 model')
            self.model_num = 1
            self.device_ids = [self.device_ids]
        else:
            self.model_num = len(self.device_ids) // tensor_parallel_size
            self.device_ids = [self.device_ids[i * tensor_parallel_size:(i + 1) * tensor_parallel_size] for i in range(self.model_num)]

            print('device num: ', len(self.device_ids))
            print('total device num: ', torch.cuda.device_count())
            print('model num: ', self.model_num)
            print('device ids: ', self.device_ids)

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.model_num) as executor:
            self.model_openais = list(executor.map(self._load_model_on_gpu, self.device_ids))

        print('*' * 100)
        print(f'Loaded {len(self.model_openais)} models')
        print(f'Used {time.time() - start_time} sec')
        print('*' * 100)
        self.last = 0


    def _read_output(self, process):
        for line in process.stdout:
            if self.show_vllm_log and line != '' :
                print(line, end='')


    def _load_model_on_gpu(self, device_ids):        
        print(f"Loading model in device {device_ids}...")
        cmd = f"export CUDA_VISIBLE_DEVICES={','.join([str(i) for i in device_ids])}\n" if not self.use_ray else f"VLLM_HOST_IP={self.ray_host_ip} VLLM_USE_RAY_SPMD_WORKER=1 VLLM_USE_RAY_COMPILED_DAG=1 "
        cmd += f"vllm serve {self.model_path} "
        cmd += f'--dtype auto --trust-remote-code '
        cmd += f'--port {self.port + device_ids[0]} '
        cmd += f'--api-key abc '
        cmd += f'--max-model-len {self.max_model_len} ' if self.max_model_len else ''
        cmd += f'--gpu-memory-utilization 0.95 '
        cmd += f'--tensor-parallel-size {self.tensor_parallel_size} '
        cmd += f'--pipeline-parallel-size {self.pipeline_parallel_size} '
        cmd += f'--enable-reasoning --reasoning-parser {self.reasoning_parser} ' if self.enable_reasoning else ''
        cmd += f'--chat-template {self.chat_template} ' if self.chat_template else ''
        cmd += f'--distributed-executor-backend ray ' if self.use_ray else ''
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.model_process.append(process)
        
        while True:
            out = process.stdout.readline()
            pid_match = re.findall(r'\(VllmWorkerProcess pid=(\d+)\)', out)
            for pid in pid_match:
                self.sub_pid.add(pid)
                
            if self.show_vllm_log and out != '':
                print(out, end='')
                
            if 'Starting vLLM API server' in out:
                print(f'Success loaded model in {device_ids}!')
                
                client = OpenAI(
                    base_url=f"http://localhost:{self.port + device_ids[0]}/v1",
                    api_key='abc'
                )
                models = client.models.list()
                model = models.data[0].id
                output_thread = threading.Thread(target=self._read_output, args=(process,))
                output_thread.daemon = True
                output_thread.start()
                return client, model

    def _cleanup(self, *args):
        for process in self.model_process:
            try:
                process.terminate()
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
        for pid in self.sub_pid:
            print(f'killing {pid}')
            os.system(f"kill -9 {pid}")

    def _signal_handler(self, signum, frame):
        self._cleanup()
        exit(0)
        
    def _except_handler(self, e):
        if isinstance(e, APIConnectionError):
            print(f'Error: "{e}", exiting')
            exit()
        else:
            print(f'Error: "{e}", retrying')
    

    def _check_custom_chat(self):
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        if self.enable_reasoning and self.reasoning_parser_obj is None:
            self.reasoning_parser_obj: ReasoningParser = ReasoningParserManager.get_reasoning_parser(self.reasoning_parser)(self.tokenizer)
            if not self.reasoning_parser_obj.think_start_token:
                raise ValueError(f"reasoning parser '{self.reasoning_parser}' should have think_start_token")
            if not self.reasoning_parser_obj.think_end_token:
                raise ValueError(f"reasoning parser '{self.reasoning_parser}' should have think_end_token")
    

    def _chat(self, item, reasoning_max_retry, param: ChatParam, ext_param: ChatExtraParam):
        connect = True
        self.last = (self.last + 1) % self.model_num
        reasoning_retry = 0
        while True:
            try:
                client, model = self.model_openais[self.last]
                completion = client.chat.completions.create(messages=item['message'], model=model, timeout=self.openai_timeout, extra_body=ext_param.__dict__, **param.__dict__)
                response = completion.choices[0].message.content
                if self.enable_reasoning:
                    reasoning = completion.choices[0].message.reasoning_content
                    if response is None or reasoning is None:
                        reasoning_retry += 1
                        if reasoning_retry <= reasoning_max_retry:
                            raise ValueError(f"{'no response' if response is None else 'no reasoning'}: {reasoning or response}, retry {reasoning_retry}")
                        item['response'] = None
                        item['reasoning'] = reasoning or response
                        return item
                break
            except Exception as e:
                self._except_handler(e)
        
        item['response'] = response
        if self.enable_reasoning:
            item['reasoning'] = reasoning
        return item

    def parallel_chat(self, messages_list, threads=20, return_dict=False, reasoning_max_retry=10, param: ChatParam=None, ext_param: ChatExtraParam=None):
        param = param if param != None else ChatParam()
        ext_param = ext_param if ext_param != None else ChatExtraParam()
        
        futures = []
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for i, msg in enumerate(messages_list):
                futures.append(executor.submit(self._chat, {'message': msg, 'idx': i}, reasoning_max_retry, param, ext_param))
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                results.append(future.result())
        results = sorted(results, key=lambda x:x['idx'])
        
        if return_dict:
            return results
        if self.enable_reasoning:
            return [(r['reasoning'], r['response']) for r in results]
        return [r['response'] for r in results]
    

    def _gen(self, item, param: GenParam, ext_param: GenExtraParam, return_completion=False):
        self.last = (self.last + 1) % self.model_num
        while True:
            try:
                client, model = self.model_openais[self.last]
                completion = client.completions.create(prompt=item['prompt'], model=model, timeout=self.openai_timeout, extra_body=ext_param.__dict__, **param.__dict__)
                break
            except Exception as e:
                self._except_handler(e)
        item['response'] = completion.choices[0].text
        if return_completion:
            return item, completion
        return item

    def parallel_generate(self, prompt_list, threads=20, return_dict=False, param: GenParam=None, ext_param: GenExtraParam=None):
        param = param if param != None else GenParam()
        ext_param = ext_param if ext_param != None else GenExtraParam()
        
        futures = []
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for i, prompt in enumerate(prompt_list):
                futures.append(executor.submit(self._gen, {'prompt': prompt, 'idx': i}, param, ext_param))
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                results.append(future.result())
        results = sorted(results, key=lambda x:x['idx'])
        
        if return_dict:
            return results
        return [r['response'] for r in results]
    
    def _chat_reasoning_length_ctrl(self, item, reasoning_max_retry, reasoning_max_len, reasoning_min_len, reasoning_scale, cut_by_sentence, param: GenParam, ext_param: GenExtraParam):
        def tlen(s):
            return len(self.tokenizer(s, add_special_tokens=False)['input_ids'])

        if reasoning_max_len and not reasoning_scale:
            reasoning_param = replace(param, max_tokens=reasoning_max_len+1)
        else:
            reasoning_param = param
        
        solution_start_token = self.reasoning_parser_obj.solution_start_token if hasattr(self.reasoning_parser_obj, 'solution_start_token') else ''
        added_think_end_token = self.reasoning_parser_obj.force_think_end_token if hasattr(self.reasoning_parser_obj, 'force_think_end_token') else self.reasoning_parser_obj.think_end_token
        
        reasoning_retry = 0
        while True:
            try:
                if (reasoning_max_len == 0 and not reasoning_scale) or reasoning_scale == 0:
                    prompt = item['prompt']
                    prompt += '' if prompt.endswith(self.reasoning_parser_obj.think_start_token) else self.reasoning_parser_obj.think_start_token
                    prompt += f'\n\n{added_think_end_token}\n\n{solution_start_token}'

                    response_param = replace(param, max_tokens=param.max_tokens - 2)
                    res_item, completion = self._gen({'prompt': prompt}, response_param, ext_param, return_completion=True)

                    if reasoning_retry < reasoning_max_retry:
                        if hasattr(self.reasoning_parser_obj, 'solution_end_token') and self.reasoning_parser_obj.solution_end_token not in res_item['response']:
                            raise ValueError('no solution_end_token')
                        if hasattr(self.reasoning_parser_obj, 'solution_start_token') and self.reasoning_parser_obj.solution_start_token in res_item['response']:
                            raise ValueError('has solution_start_token')
                        if self.reasoning_parser_obj.think_end_token in res_item['response']:
                            raise ValueError('has think_end_token')
                    
                    response = f"{self.reasoning_parser_obj.think_start_token}\n\n{added_think_end_token}\n\n{solution_start_token}{res_item['response']}"

                    reasoning, response = self.reasoning_parser_obj.extract_reasoning_content(response, completion)
                    if response is None:
                        raise ValueError(f'bad reasoning: {reasoning_retry}')
                    break
                
                res_item, completion = self._gen(item, reasoning_param, ext_param, return_completion=True)
                response = res_item['response']
                if self.reasoning_parser_obj.think_end_token not in response:
                    response += self.reasoning_parser_obj.think_end_token

                rean, resp = self.reasoning_parser_obj.extract_reasoning_content(response, completion)
                prompt = item['prompt'] + ('' if item['prompt'].endswith(self.reasoning_parser_obj.think_start_token) else self.reasoning_parser_obj.think_start_token)

                if reasoning_scale > 1:
                    reasoning_min_len = tlen(rean) * reasoning_scale
                if reasoning_scale < 1:
                    rean_token = self.tokenizer(rean, add_special_tokens=False)['input_ids']
                    rean_token = rean_token[:int(len(rean_token)*reasoning_scale)]
                    rean = self.tokenizer.decode(rean_token)

                if cut_by_sentence:
                    rean = rean.rsplit('.', 1)[0] + '.'

                reasoning = rean
                while reasoning_scale > 1 and tlen(reasoning) < reasoning_min_len:
                    prompt += f"{rean}{self.more_reasoning_prompt}"
                    if reasoning_max_len and not reasoning_scale:
                        reasoning_param = replace(param, max_tokens=reasoning_max_len - tlen(reasoning) - tlen(self.more_reasoning_prompt))
                    res_item, completion = self._gen({'prompt': prompt}, reasoning_param, ext_param, return_completion=True)
                    response = res_item['response']
                    rean, resp = self.reasoning_parser_obj.extract_reasoning_content(response, completion)
                    reasoning += f"{self.more_reasoning_prompt}{rean}"
                    if cut_by_sentence:
                        reasoning = reasoning.rsplit('.', 1)[0] + '.'

                prompt += f"{rean}\n\n{added_think_end_token}\n\n"
                
                if param.max_tokens != None:
                    response_param = replace(param, max_tokens=param.max_tokens - tlen(reasoning) - 2)
                res_item, completion = self._gen({'prompt': prompt}, response_param, ext_param, return_completion=True)
                response = res_item['response']
                response = f"{self.reasoning_parser_obj.think_start_token}{reasoning}{added_think_end_token}{response}"
                reasoning, response = self.reasoning_parser_obj.extract_reasoning_content(response, completion)

                if response is None or reasoning is None:
                    raise ValueError(f'bad reasoning: {reasoning_retry}')
                break
            except Exception as e:
                print(f'Error: {e}, retried {reasoning_retry} times')
                reasoning_retry += 1
                if reasoning_retry > reasoning_max_retry:
                    item['response'] = None
                    item['reasoning'] = reasoning or response
                    return item
        
        item['response'] = response
        item['reasoning'] = reasoning
        return item
    
    def _chat_reasoning(self, item, reasoning_max_retry, param: GenParam, ext_param: GenExtraParam):
        reasoning_retry = 0
        while True:
            try:
                item, completion = self._gen(item, param, ext_param, return_completion=True)
                response = item['response']
                reasoning, response = self.reasoning_parser_obj.extract_reasoning_content(response, completion)
                if response is None or reasoning is None:
                    reasoning_retry += 1
                    if reasoning_retry <= reasoning_max_retry:
                        raise ValueError(f'bad reasoning: {reasoning_retry}')
                    item['response'] = None
                    item['reasoning'] = reasoning or response
                    return item
                break
            except Exception as e:
                self._except_handler(e)
        
        item['response'] = response
        item['reasoning'] = reasoning
        return item
  

    def parallel_chat_custom(self, messages_list, threads=20, reasoning_max_retry=10, add_reasoning_prompt=False, enable_length_ctrl=False, reasoning_max_len: int=None, reasoning_min_len: int=0, reasoning_scale: float=None, cut_by_sentence: bool = False, return_dict=False, param: GenParam=None, ext_param: GenExtraParam=None):
        self._check_custom_chat()

        param = param if param != None else GenParam()
        ext_param = ext_param if ext_param != None else GenExtraParam()
        prompt_list = self.tokenizer.apply_chat_template(messages_list, tokenize=False, add_generation_prompt=True)
        
        if not self.enable_reasoning:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                for i, prompt in enumerate(prompt_list):
                    futures.append(executor.submit(self._gen, {'prompt': prompt, 'idx': i}, param, ext_param))
                
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    results.append(future.result())
            results = sorted(results, key=lambda x:x['idx'])
            if return_dict:
                return results
            return [r['response'] for r in results]
        

        if add_reasoning_prompt:
            prompt_list = [p if p.endswith(self.reasoning_parser_obj.think_start_token) else (p + self.reasoning_parser_obj.think_start_token) for p in prompt_list]

        if enable_length_ctrl:
            if reasoning_max_len is not None and reasoning_max_len < reasoning_min_len:
                raise ValueError(f"reasoning_min_len({reasoning_min_len}) should less than reasoning_max_len({reasoning_max_len})")
            if reasoning_scale:
                print("Setted reasoning_scale, ignore reasoning_max_len and reasoning_min_len")
            
            futures = []
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                for i, prompt in enumerate(prompt_list):
                    futures.append(executor.submit(self._chat_reasoning_length_ctrl, {'prompt': prompt, 'idx': i}, reasoning_max_retry, reasoning_max_len, reasoning_min_len, reasoning_scale, cut_by_sentence, param, ext_param))
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    results.append(future.result())
        else:
            futures = []
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                for i, prompt in enumerate(prompt_list):
                    futures.append(executor.submit(self._chat_reasoning, {'prompt': prompt, 'idx': i}, reasoning_max_retry, param, ext_param))
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    results.append(future.result())
        
        results = sorted(results, key=lambda x:x['idx'])
        
        if return_dict:
            return results
        return [(r['reasoning'], r['response']) for r in results]
    
            
    def parallel_chat_force_reasoning_content(self, messages_list, reasoning_content, threads=20, reasoning_scale: float=None, cut_by_sentence: bool = False, return_dict=False, param: GenParam=None, ext_param: GenExtraParam=None):
        self._check_custom_chat()
        if reasoning_scale is not None:
            if reasoning_scale > 1:
                raise ValueError("Only support to cut off exist reasoning content")
            
            reasoning_content_tokens = self.tokenizer(reasoning_content, add_special_tokens=False)['input_ids']
            reasoning_content_tokens = [r[:int(len(r) * reasoning_scale)] for r in reasoning_content_tokens]
            reasoning_content = [self.tokenizer.decode(r) for r in reasoning_content_tokens]
            if cut_by_sentence: 
                reasoning_content = [r.rsplit('.', 1)[0]+'.' for r in reasoning_content]
        

        param = param if param != None else GenParam()
        ext_param = ext_param if ext_param != None else GenExtraParam()
        
        solution_start_token = '\n\n' + self.reasoning_parser_obj.solution_start_token if hasattr(self.reasoning_parser_obj, 'solution_start_token') else ''
        
        prompt_list = self.tokenizer.apply_chat_template(messages_list, tokenize=False, add_generation_prompt=True)
        prompt_list = [f'{p}{"" if p.endswith(self.reasoning_parser_obj.think_start_token) else self.reasoning_parser_obj.think_start_token}\n\n{r}\n\n{self.reasoning_parser_obj.think_end_token}{solution_start_token}' for p, r in zip(prompt_list, reasoning_content)]
        
        futures = []
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for i, prompt in enumerate(prompt_list):
                futures.append(executor.submit(self._gen, {'prompt': prompt, 'idx': i}, param, ext_param))
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                results.append(future.result())
        results = sorted(results, key=lambda x:x['idx'])
        if return_dict:
            return results
        return [(rean, r['response']) for rean, r in zip(reasoning_content, results)]
        


if __name__ == "__main__":
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/s1.1-32B"
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/Meta-Llama-3-8B-Instruct"
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/DeepSeek-R1-Distill-Qwen-7B"
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/Meta-Llama-3-70B-Instruct"
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/DeepSeek-R1-Distill-Qwen-32B"
    model_path = "/share/home/wxzhao/gjh_ws/Downloads/LLMs/Qwen2.5-32B-Instruct"
    # model_path = "/share/home/wxzhao/gjh_ws/Downloads/R1/DeepSeek-R1"
    # df = pd.read_csv('/share/home/wxzhao/decode/my_decode/query/strongreject_small_dataset.csv')
    # data = df.to_dict(orient='records')
    # data = [[{'role': 'user', 'content': d['forbidden_prompt']}] for d in data]
    data = [[{'role': 'user', 'content': "Write a 300+ word summary of the wikipedia page \"https://en.wikipedia.org/wiki/Raymond_III,_Count_of_Tripoli\". Do not use any commas and highlight at least 3 sections that has titles in markdown format, for example *highlighted section part 1*, *highlighted section part 2*, *highlighted section part 3*."}] for _ in range(10)]

    # inference_system = InferenceModel(model_path, tensor_parallel_size=8, max_model_len=10000)
    inference_system = InferenceModel(model_path, tensor_parallel_size=4, device_ids=[0,1,2,3], max_model_len=10000)
    # inference_system = InferenceModel(model_path, tensor_parallel_size=8, pipeline_parallel_size=2, show_vllm_log=True, openai_timeout=1000, enable_reasoning=False, max_model_len=10000, use_ray=True, port=45697, ray_host_ip='172.16.1.76')
    results = inference_system.parallel_chat(data, threads=10, param=ChatParam(max_completion_tokens=512))
    print(results[0])

    # with open('/share/home/wxzhao/decode/my_decode/test.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)

    # for i, result in enumerate(results):
    #     print(f"Result {i+1}: {result}")


    # data = df.to_dict(orient='records')[:10]
    # data = [d['forbidden_prompt'] for d in data]
    # results = inference_system.parallel_generate(data, threads=100, param=GenParam(max_tokens=4096))
    # for i, result in enumerate(results):
    #     print(f"Result {i+1}: {result}")
