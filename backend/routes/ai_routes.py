from flask import Blueprint, request, jsonify

ai_bp = Blueprint('ai', __name__)

sample_descriptions = {
    'Workshop': "An interactive workshop designed to enhance your skills.",
    'Conference': "A professional conference featuring expert speakers and networking opportunities.",
    'Seminar': "A seminar providing deep insight into the latest trends.",
    'Social': "A fun and engaging social event to meet new people.",
    'Concert': "A live concert that will keep you entertained all night!"
}

# @ai_bp('/api/ai/generate-description', methods=['POST'])
# def generate_event_description():
#     try:
#         data = request.get_json()
#         title = data.get('title')

#         if not title:
#             return jsonify({'message': 'Title is required to generate a description'}), 400

#         prompt = (
#             f"Write a professional, engaging, and concise description for an event titled '{title}'. "
#             "Highlight what makes the event interesting or valuable to potential attendees."
#         )

#         # --- FIX: UPDATED GOOGLE GEMINI MODEL NAME ---
#         # The 'gemini-pro' model is outdated. Using a current model like 'gemini-1.5-flash-latest'.
#         model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
#         response = model.generate_content(prompt)
        
#         return jsonify({'description': response.text.strip()}), 200

#     except Exception as e:
#         print(f"AI Generation Error: {e}")
#         return jsonify({'message': f'Failed to generate AI description: {str(e)}'}), 500

@ai_bp.route('/api/ai/description', methods=['POST'])
def generate_description():
    data = request.json
    title = data.get('title', '')
    category = data.get('category', 'Conference')

    base = sample_descriptions.get(category, "A special event you won’t want to miss.")
    return jsonify({'description': f"{base}."})

