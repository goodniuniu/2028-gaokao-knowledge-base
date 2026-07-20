import os
import subprocess

d = r'C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库'
os.chdir(d)

# git status
print("=== Git Status ===")
result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
print(result.stdout if result.stdout else "(无未跟踪改动)")

# git add
print("\n=== Git Add ===")
result = subprocess.run(['git', 'add', '图形库/'], capture_output=True, text=True)
print(result.stdout if result.stdout else "已添加图形库目录")

# git commit
print("\n=== Git Commit ===")
result = subprocess.run(['git', 'commit', '-m', 'feat: 新增高考知识库知识点示意图16张（物理4+化学4+生物4+数学4）'],
                        capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# git push
print("\n=== Git Push ===")
result = subprocess.run(['git', 'push'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
