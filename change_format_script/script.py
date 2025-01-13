from markitdown import MarkItDown

file_path = input()
md = MarkItDown()
result = md.convert(file_path)
print(result.text_content)
