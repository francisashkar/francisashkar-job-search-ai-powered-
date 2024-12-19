# AI-Powered Job Search Application

An intelligent job search platform that uses OpenAI's GPT-4 to understand and interpret user queries, providing more relevant job search results. The application features a clean, modern interface and uses MongoDB for data storage.

## Features

- Natural language job search powered by GPT-4
- Intelligent keyword extraction and intent inference
- Clean, responsive user interface
- MongoDB integration for efficient job data storage
- Pagination support for search results
- Real-time search suggestions and instructions

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **AI Integration**: OpenAI GPT-4
- **Additional Libraries**: 
  - Flask-CORS for cross-origin resource sharing
  - PyMongo for MongoDB integration

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7+
- MongoDB
- pip (Python package manager)

You'll also need:
- An OpenAI API key
- MongoDB connection URI

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key and MongoDB URI:
```
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri
```

## Configuration

1. Update the MongoDB connection settings in `app.py`:
   - Modify the MongoDB URI
   - Update the database and collection names as needed

2. Configure the OpenAI API settings:
   - Adjust the model parameters in the `extract_keywords_with_openai` function
   - Modify the system prompt as needed

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter your job search query in the search bar
2. The application will:
   - Extract relevant keywords using GPT-4
   - Search the MongoDB database for matching jobs
   - Display results in a paginated format
3. Click the info icon (i) for search tips and examples

## Security Notes

- Remove or secure the API keys before deploying
- Update the CORS settings in production
- Implement proper error handling and input validation
- Consider adding rate limiting for the API endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- MongoDB for the database solution
- Flask community for the excellent web framework
