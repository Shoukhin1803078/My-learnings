# Interview question

1. What's the difference between fine-tuning and RAG?
2. Why are transformers better than LSTMs?
3. What’s LoRA and QLoRA?
4. Text-to-text vs. multimodal generation?
5. Which method is used to remove stop words in AI.
6. What is semantic search?
7. What is Tokenization and how it differs from Lemmetization?



# Python/Django Interview Question:

# **Backend API Development (Python/Django) Interview Questions & Answers**

**1. What are Django views?**

* **Views are Python functions or classes that take a request and return a response (HTML, JSON, etc.).**

##### **2. What is the difference between Function-Based Views (FBV) and Class-Based Views (CBV)?**

* **FBV** **→ Simple, procedural, easy for small logic.**
* **CBV** **→ OOP-style, reusable, good for large apps with inheritance.**

##### **3. How do you map URLs to views in Django?**

* **Use** `urls.py` **with** `path()` **or** `re_path()`.

`path('home/', views.home, name='home'`)

##### **4. How do you pass data from view to template?**

`def home(request`):
`return render(request, 'home.html', {'name': 'Rahim'`})

##### **5. How do you return JSON data from a view?**

`from django.http import` **JsonResponse**
`def api_view(request`):
`return JsonResponse({'status': 'ok'`})

##### **6. What is the difference between ****`render()`**** and ****`redirect()`****?**

* `render()` **→ Renders template with context.**
* `redirect()` **→ Redirects user to another URL/view.**

##### **7. How do you handle GET and POST requests in Django view?**

`def contact(request`):
`if request.method == 'POST'`:
`# handle form submission`
`else`:
`# show form`

##### **8. What are generic class-based views (CBVs) in Django?**

* **Prebuilt views like** `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.

##### **9. How do you restrict access to a view (authentication)?**

* **Using decorator:**

`from django.contrib.auth.decorators import` **login_required**
`@login_required`
`def dashboard(request`):
...

##### **10. How do you return a 404 error in a view?**

`from django.shortcuts import` **get_object_or_404**
`product = get_object_or_404(Product, id=1)`

***Learn "**Django &** **Backend API Development with Python**"
**> Check Comment box**
