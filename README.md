ARYA Ai - A Hostel Helping AI Bot
=================================

**ARYA Ai** is a conversational assistant designed to help hostel residents with inquiries, rules, and complaint management. It utilizes state-of-the-art machine learning models and retrieval-based generation techniques to provide accurate, real-time information to users.

<!-- Optional: Add a bot logo or a screenshot of your bot interface -->

Features
--------

-   **Query Answering**: Provides instant answers to hostel-related queries such as rules, guidelines, and available facilities.
-   **Complaint Management**: Allows users to submit complaints, track their status, and receive updates in real-time.
-   **Conversational Context**: Leverages Langchain for handling multi-turn conversations, improving user interaction.
-   **Knowledge Base**: Uses Pinecone to store and retrieve hostel-related information efficiently.
-   **User-Friendly Interface**: Deployed using Streamlit to ensure smooth user interaction and accessibility.

Technologies Used
-----------------

-   **MixRtral8x76**: A pre-trained transformer model from Hugging Face used for natural language understanding.
-   **RAG (Retrieval-Augmented Generation)**: Combines document retrieval and text generation for accurate and context-aware responses.
-   **Pinecone**: A vector database that stores information for fast retrieval, enhancing the bot's response speed.
-   **Langchain**: A framework for managing conversational agents and maintaining context throughout interactions.
-   **Streamlit**: Deployed with Streamlit to provide an easy-to-use web interface for users.

Installation
------------

1.  **Clone the repository**:

    bash

    Copy code

    `git clone https://github.com/your_username/arya-ai-bot.git
    cd arya-ai-bot`

2.  **Install the required dependencies**:

    bash

    Copy code

    `pip install -r requirements.txt`

3.  **Set up Pinecone**:

    -   Sign up for a [Pinecone](https://www.pinecone.io/) account.

    -   Get your API key and set it up in your environment:

        bash

        Copy code

        `export PINECONE_API_KEY=your_api_key`

4.  **Run the bot**:

    bash

    Copy code

    `streamlit run app.py`

Usage
-----

Once the application is running, you can interact with Arya Ai via the web interface. Simply type in your query or complaint, and the bot will respond accordingly.

### Example Queries

-   "What are the hostel rules?"
-   "How do I file a complaint?"
-   "What time is the hostel curfew?"

### Example Complaint

-   "I would like to report a broken window in room 302."

File Structure
--------------

bash

Copy code

`arya-ai-bot/
├── app.py                 
├── requirements.txt        
├── data/                    
├── models/                 
├── utils/                   
└── README.md                

Future Enhancements
-------------------

-   **Multi-language Support**: Expand the bot to handle multiple languages.
-   **Sentiment Analysis**: Analyze the sentiment of user queries to offer better support in cases of urgent complaints.
-   **Voice Input**: Integrate voice recognition for more natural interaction with users.

Contributing
------------

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

License
-------

This project is licensed under the Apache License - see the LICENSE file for details.
