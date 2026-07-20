import subprocess, os
d = r'C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库'
result = subprocess.run(['git','-C',d,'log','--oneline','-3'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
print(result.stdout)
