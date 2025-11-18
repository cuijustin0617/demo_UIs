# RA-Rec Demo UI

Demo visualization for **RA-Rec: Retrieval-Augmented Conversational Recommendation with Prompt-based Semi-Structured State**

## About

This interactive demo showcases the RA-Rec system, which uses retrieval-augmented generation for conversational restaurant recommendations. The demo illustrates:

- **Semi-structured state tracking** with hard and soft constraints
- **Late fusion retrieval** process using review-level scoring
- **Grounded generation** for natural recommendation responses

**Authors:** Sara Kemper*, Justin Cui*, Kai Dicarlantonio*, Kathy Lin*, Danjie Tang*, Anton Korikov, Scott Sanner  
*Equal Contribution | University of Toronto & University of Waterloo | SIGIR '24

📄 [Read the Paper](https://arxiv.org/abs/2406.00033) | 💻 [GitHub Repository](https://github.com/D3Mlab/llm-convrec)

## Live Demo

🚀 [View Live Demo](#) *(Add your deployment URL here)*

## Running Locally

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/demo_UIs.git
cd demo_UIs/llm_convrec_viz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment

This app can be easily deployed to:
- **Streamlit Cloud** (recommended, free)
- **Heroku**
- **Railway**
- **Google Cloud Run**

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and branch
5. Set the main file path to `llm_convrec_viz/app.py`
6. Click Deploy!

## Project Structure

```
demo_UIs/
└── llm_convrec_viz/
    ├── app.py           # Main Streamlit application
    └── requirements.txt  # Python dependencies
```

## Citation

If you find this work useful, please cite:

```bibtex
@inproceedings{kemper2024rarec,
  title={RA-Rec: Retrieval-Augmented Conversational Recommendation with Prompt-based Semi-Structured State},
  author={Kemper, Sara and Cui, Justin and Dicarlantonio, Kai and Lin, Kathy and Tang, Danjie and Korikov, Anton and Sanner, Scott},
  booktitle={SIGIR},
  year={2024}
}
```

## License

MIT License

