from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz
import re

app = Flask(__name__)

GREETINGS = ['hello', 'hi', 'help', 'hii', 'hiii']
FAQ = {
    "What's this 'Shut up and Wait for your Zone' all about?":
    "Oh, it's a cool trading course that teaches you everything from the basics to the advanced stuff, focusing on nailing those perfect trading moments 📈.",
    "Who should totally check out this course?":
    "Anyone who wants to level up in trading, really. Whether you're just starting out or you've been at it for a while but wanna refine your tactics 🔄.",
    "What kind of trading magic will I learn?":
    "You'll dive into all sorts of strategies, like mastering price actions, learning top-notch risk management, and understanding the charts like a pro. It's all about patience and picking the right moments ⏳. That's why we named 'Shut up and wait for your Zone' - We teach the magic of this term.",
    "Can I juggle this with my nine-to-five?":
    "Absolutely, yes! The course is super flexible. You can access the material whenever fits your schedule best, so no stress there 🎒.",
    "What do I need to get started?":
    "Just a good internet connection and any device that lets you watch videos and hop on our website. Super simple 👌.",
    "How do I jump into this course?":
    "Just pop over to our website, fill out the sign-up form, pick your membership, and you're all set to start learning 📚.",
    "What's the damage (aka cost)?":
    "You've got two cool options: Full Course: One-time payment of ₹15,999 for complete access 🎫. Pay Per Video: Flexibility to pay only for the videos you watch, great for trying out or if you're not ready to dive all in 📺.",
    "What if I'm not feeling it?":
    "No worries, we've got a refund policy. Check out the terms on our site, but we're pretty sure you're gonna love it ❤️.",
    "Something's bugging me, who do I shout out to?":
    "Hit up our support team anytime through the 'Contact Us' page. We've got email, phone, and even live chat. Whatever works for you 🤝!",
    "What perks do I get with the membership levels?":
    "More goodies as you go up the tiers! Things like exclusive materials, personal sessions with trainers, and members-only content. Choose what fits your vibe ✨.",
    "What security measures are in place for my data?":
    "We take your privacy super seriously. Our site uses the latest security tech to keep your personal and payment info safe and sound.",
    "Can I get a sneak peek before I buy?":
    "Sure thing! Check out some free sample videos on our website and social media to see if it's your cup of tea before you commit.",
    "Are there any group discounts available?":
    "Yep, we offer sweet deals for groups. Gather your friends or colleagues and save some cash when you sign up together. Limited time offer. T&C",
    "How long do I have access to the course materials?":
    "Once you're in, you have unlimited access to the course materials for 90 days from the date of purchase of the course—watch and rewatch as much as you like.",
    "Expire how much date duration access":
    "Once you're in, you have unlimited access to the course materials for 90 days from the date of purchase of the course—watch and rewatch as much as you like.",
    "Who are the trainers?":
    "Our trainers are seasoned traders with years of experience. They're here to share real-world insights and help you master the markets.",
    "What is the course about?":
    "The course 'Shut up and Wait for your Zone' is a comprehensive trading course designed to teach you everything from the basics to advanced strategies in the stock market.",
    "How is the course structured?":
    "The course is divided into modules covering different aspects of trading, including technical analysis, risk management, psychology, and more.",
    "What level of experience is required?":
    "The course is suitable for both beginners and experienced traders who want to refine their skills and strategies.",
    "Is there a certification after completing the course?":
    "Yes, upon successful completion of the course, you will receive a certificate of completion.",
    "How is the course delivered?":
    "The course is delivered through a combination of video lectures, interactive exercises, quizzes, and optional assignments.",
    "Can I access the course on mobile devices?":
    "Yes, the course materials are accessible on both desktop and mobile devices, allowing you to learn on-the-go.",
    "Is there a money-back guarantee?":
    "Yes, we offer a money-back guarantee if you're not satisfied with the course within a certain period of time. Please check our website for the specific terms and conditions.",
    "Are there any prerequisites for the course?":
    "No formal prerequisites are required, but some basic knowledge of financial markets and trading would be beneficial.",
    "How long does it take to complete the course?":
    "The duration of the course depends on your pace and dedication. Most students complete it within 3-6 months, but you have access for 90 days from the date of purchase.",
    "Is there a community or support system?":
    "Yes, we have an active community forum where you can interact with fellow students, ask questions, and receive guidance from our experts."
}


@app.route('/')  # This is the homepage
def index():
    return render_template(
        'index.html'
    )  # The spot where it says 'index.html' is what HTML file loads.


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data['query']

    # Here you can implement your chatbot logic
    response = respond_to_query(query)

    return jsonify(response)


def respond_to_query(query):
    # Check if the query is a greeting
    if query.lower() in GREETINGS:
        return {
            'type': 'msg',
            'response':
            'Welcome to our Stock Market course, how can I help you?'
        }
    else:
        matched_question = max(
            FAQ.keys(), key=lambda key: fuzz.token_set_ratio(query, key))
        similarity_score = fuzz.token_set_ratio(query, matched_question)

        if similarity_score >= 50:  # Adjust the threshold as needed
            return {'type': 'msg', 'response': FAQ[matched_question]}
        else:
            matched_questions = [
                key for key in FAQ.keys()
                if fuzz.token_set_ratio(query, key) >= 40
            ]  # Adjust threshold as needed
            if matched_questions:
                return {'type': 'question', 'response': matched_questions}
            else:
                # Search for questions containing any word of the query
                query_words = re.findall(r'\w+', query.lower())
                matched_questions = [
                    key for key in FAQ.keys() for word in query_words
                    if word in key.lower()
                ]

                if matched_questions:
                    return {
                        'type': 'question',
                        'response': list(set(matched_questions))
                    }
                else:
                    # Try to match keywords in the query
                    query_keywords = [
                        word for word in query_words if word not in [
                            'is', 'what', 'how', 'a', 'the', 'and', 'or', 'to',
                            'for', 'of', 'in', 'on', 'at', 'by', 'from', 'with'
                        ]
                    ]
                    matched_questions = [
                        key for key in FAQ.keys() for keyword in query_keywords
                        if keyword in key.lower()
                    ]

                    if matched_questions:
                        return {
                            'type': 'question',
                            'response': list(set(matched_questions))
                        }
                    else:
                        return {
                            'type':
                            'msg',
                            'response':
                            'Sorry, I couldn\'t find a relevant answer to your query. Please try rephrasing your question or ask for specific topics you\'re interested in.'
                        }


if __name__ == '__main__':
    app.run(
        debug=True, host='0.0.0.0', port="2048"
    )  # Debug reloads when a change is made to the code. Turn it off to edit without changes
