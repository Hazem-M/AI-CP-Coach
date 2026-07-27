# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Hazem [أكمل اسمك هنا]                |
| Project Name     | AI CP Coach (Competitive Programming Coach) |
| GitHub Username  | [اكتب اليوزر نيم بتاعك هنا]          |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**AI CP Coach** is an advanced AI-powered assistant designed specifically for Competitive Programming. Instead of just giving out the answers, it acts as a "Socratic Grandmaster", breaking down complex problems, providing progressive hints without spoiling the solution, and rigorously reviewing users' code for bugs, Time Limit Exceeded (TLE) risks, and styling issues. 

The project leverages a highly capable LLM (`Qwen2.5-Coder-7B-Instruct`) and LangChain to orchestrate specialized AI chains, presented through a clean, interactive Streamlit Web UI.

---

# ✨ Features

* **🧠 Problem Analysis:** Instantly breaks down competitive programming problems into core algorithmic ideas, time/space complexities, and edge cases.
* **💡 Progressive Hints:** Stuck on a problem? The coach provides tiered hints (Nudge ➡️ Approach ➡️ Detailed ➡️ Solution) to guide your thinking process without immediately giving away the code.
* **✅ AI Code Reviewer:** Submits user code against the problem statement for a comprehensive review. Identifies critical bugs, warns about TLE risks, provides optimization suggestions, and grades the solution out of 100.
* **🤔 AI Thinking Process:** Transparently displays the AI's internal reasoning (`<think>` tags) before revealing the final answer.

---

# 🛠️ Technologies Used

* **Python 3.12**
* **Streamlit** (Frontend UI framework)
* **LangChain** (LLM orchestration and prompt engineering)
* **Hugging Face Transformers** (Model loading and pipeline integration)
* **Qwen2.5-Coder-7B-Instruct** (Base Large Language Model)
* **PyTorch** (Deep learning framework)

---

# ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/[Your-Username]/AI-CP-Coach.git
   cd AI-CP-Coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

*(Note: Running this locally requires a machine capable of running 7B parameter models, or it can be run via Google Colab).*

---

# 🚀 Usage

1. Open the web interface in your browser.
2. **Analyze Page:** Paste a Codeforces/LeetCode problem statement and let the AI break it down for you.
3. **Hints Page:** Paste a problem and click to reveal hints one by one as you try to solve it yourself.
4. **Review Page:** Paste the problem along with your written C++, Python, or Java code. The AI will critique your solution and find potential bugs.

---

# 📸 Demo

*(Add the amazing screenshots you took today of the working Analyze, Hints, and Review pages here!)*

---

# 📈 Results

* Successfully built an end-to-end AI coaching system that parses complex logic.
* Mitigated model hallucination and forced strict structured outputs by applying robust Prompt Engineering techniques.
* Developed an elegant UI that seamlessly parses AI reasoning processes and cleanly formats code snippets with syntax highlighting.

---

# 🔮 Future Improvements

* Integrate **RAG (Retrieval-Augmented Generation)** to fetch related Codeforces tutorials and similar problems directly from a vector database.
* Connect to the official **Codeforces API** to fetch user profiles, track rating changes, and recommend tailored practice problems based on weaknesses.
* Deploy the application live on a cloud platform like Hugging Face Spaces or AWS.

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
