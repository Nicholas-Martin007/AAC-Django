# Backend LLM Django

Repository ini digunakan untuk menjalankan **backend Django** yang terintegrasi dengan **Large Language Model (LLM)**.

---

## 🖥️ Persyaratan Sistem

Untuk menjalankan server backend dan pemrosesan berbasis LLM, dibutuhkan spesifikasi perangkat keras berikut:

* **Processor**: Intel Core i9-11900H
* **GPU**: NVIDIA RTX 3060 (6 GB VRAM)
* **RAM**: 16 GB DDR4 3200 MHz

> ⚠️ GPU NVIDIA direkomendasikan untuk performa optimal saat menjalankan model LLM.

---

## 🤖 Setup Model

1. Unduh model dasar secara manual melalui Hugging Face:

   * **LLaMA 3.2 3B Instruct**
     [https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)

2. Untuk model yang telah dilakukan *fine-tuning*, silakan unduh file model melalui tautan berikut:

   * **LLaMA 3.2 3B (Fine-Tuned)**
     `https://drive.google.com/drive/folders/1x5uzL9SEvdquhbx9rctEY9DxijIjtnwA`

---

## 🚀 Menjalankan Backend Server

Setelah seluruh proses setup selesai, jalankan backend server dengan perintah berikut:

```bash
python manage.py runserver
```

Backend server akan berjalan secara default pada:

```
http://127.0.0.1:8000/ atau http://localhost:3000/
```

---

## 📦 Persyaratan Khusus

Seluruh package Python yang dibutuhkan tercantum pada file `requirements.txt`.

### Catatan Penting

* Untuk menjalankan **Flan-T5**, diperlukan versi terbaru dari beberapa package berikut:

```bash
pip install -U transformers peft accelerate bitsandbytes
```

* Untuk model **LLaMA, Mistral, dan model lainnya**, dapat menggunakan versi stabil berikut:

```bash
pip install transformers==4.53.2 peft==0.17.1 accelerate==1.10.1 bitsandbytes==0.47.0
```

---

## 📘 Manual Book

Panduan penggunaan sistem secara lengkap dapat dilihat pada file berikut:

- **Manual Book**: `535220027_Manual Book.pdf`
