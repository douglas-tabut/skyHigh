import re
text = "Hello, my name is John and I live in Toronto. I like playing basketball and soccer"

pattern = r'\b(\w+)\s+(\w+)\b'
names = re.findall(pattern, text)

print(names)