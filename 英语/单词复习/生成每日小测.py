#!/usr/bin/env python3
"""生成每日单词小测卷 - 用法: python 生成每日小测.py <Day编号>"""
import random, os, sys

def generate_quiz(day_num, num_questions=20):
    base = os.path.dirname(os.path.abspath(__file__))
    word_file = os.path.join(base, "分组词表", f"Day_{day_num:03d}.md")
    
    if not os.path.exists(word_file):
        print(f"错误：Day {day_num} 词汇表不存在")
        return
    
    words = []
    with open(word_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('|') and '**' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    word = parts[2].replace('**', '').strip()
                    meaning = parts[3].strip()
                    words.append((word, meaning))
    
    if len(words) < num_questions:
        print(f"词汇量不足：{len(words)} < {num_questions}")
        return
    
    selected = random.sample(words, num_questions)
    
    quiz_path = os.path.join(base, "小测卷", f"Day_{day_num:03d}_小测.md")
    ans_path = os.path.join(base, "小测卷", f"Day_{day_num:03d}_答案.md")
    
    with open(quiz_path, 'w', encoding='utf-8') as f:
        f.write(f"# Day {day_num} 单词小测\n\n")
        f.write(f"> 日期：_______  |  用时：_______  |  正确率：_______\n\n")
        f.write("## 一、英译汉（写出中文意思）\n\n")
        for i, (w, m) in enumerate(selected[:10], 1):
            f.write(f"{i}. **{w}**  _________________________\n\n")
        f.write("## 二、汉译英（根据释义写出单词）\n\n")
        for i, (w, m) in enumerate(selected[10:], 1):
            f.write(f"{i}. {m}  _________________________\n\n")
        f.write("---\n\n> **批改后**：把错题单词抄入错题本，明天先复习这些词。\n")
    
    with open(ans_path, 'w', encoding='utf-8') as f:
        f.write(f"# Day {day_num} 单词小测答案\n\n")
        for i, (w, m) in enumerate(selected[:10], 1):
            f.write(f"{i}. {w} — {m}\n")
        f.write("\n")
        for i, (w, m) in enumerate(selected[10:], 1):
            f.write(f"{i}. {m} — {w}\n")
    
    print(f"已生成：Day {day_num} 小测卷 + 答案")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        day = int(sys.argv[1])
        generate_quiz(day)
    else:
        print("用法：python 生成每日小测.py <Day编号>")
        print("示例：python 生成每日小测.py 11")
