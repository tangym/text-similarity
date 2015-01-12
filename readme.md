## 说明
根据两个字符串的编辑距离(Levenshtein distance)，计算字符串的相似度。
$$
similarity = \frac{1}{1+Levenshtein(s_1, s_2)}
$$

## 步骤

1. POST一个包含参数的JSON字符串

```
{
    "query" : "decf",
    "document": "abcdefg"
}
```

2. 返回错误信息或相似度

```
{
    "error message": "msg"
}
```
```
{
    "similarity": 0.500
}
```

## Requirements

Flask==0.10.1
Jinja2==2.7.3
Merkzeug==0.9.6
python-Levenshtein==0.11.2


