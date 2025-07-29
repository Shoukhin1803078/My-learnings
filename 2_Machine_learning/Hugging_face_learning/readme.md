#### **Hugging face login way from colab notebook or terminal:**

**way-1:**

```
from huggingface_hub import  
notebook_loginnotebook_login()
```

**way-2:**

```
import os
os.environ['HF_TOKEN'] = 'YOUR_TOKEN_HERE'
```

**Way-3:**
