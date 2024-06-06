import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login_page'
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'ratings_board' not in st.session_state:
    st.session_state.ratings_board = {}
if 'ratings_peer' not in st.session_state:
    st.session_state.ratings_peer = {}
if 'ratings_chairman' not in st.session_state:
    st.session_state.ratings_chairman = {}
if 'ratings_trustee' not in st.session_state:
    st.session_state.ratings_trustee = {}
if 'ratings_committee' not in st.session_state:
    st.session_state.ratings_committee = {}
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = False

# Define names, usernames, and plain text passwords
names = ["Albert Ambune", "Winnie Mwangi", "Job Makanga", "Grace Akinyi", "Vincent Chagara", "Kennedy Odede", "Ruth Mbithe", "Dr. Kamuri"]
usernames = ["albertambune", "winniemwangi", "jobmakanga", "graceakinyi", "vincentchagara", "kennedyodede", "ruthmbithe", "drkamuri"]
passwords = ["albertambune_24", "winniemwangi_24", "jobmakanga_24", "graceakinyi_24", "vincentchagara_24", "kennedyodede_24", "ruthmbithe_24", "drkamuri_24"]

# Hash the passwords
hashed_passwords = [bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') for password in passwords]

# Function to authenticate users
def authenticate(username, password):
    if username in usernames:
        user_index = usernames.index(username)
        return bcrypt.checkpw(password.encode('utf-8'), hashed_passwords[user_index].encode('utf-8'))
    return False

# Streamlit login form
def login_page():
    st.markdown("<h1>KNH 2024 BOARD EVALUATION & PEER REVIEW</h1>", unsafe_allow_html=True)

    if st.session_state.authentication_status:
        st.sidebar.success(f"Welcome, {st.session_state.name}")

        # Add logout button
        if st.sidebar.button("Logout"):
            st.session_state.authentication_status = False
            st.session_state.name = ""
            st.session_state.username = ""
            st.session_state.current_page = "login_page"
            st.sidebar.warning("You have been logged out.")
    else:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", type='password', key="login_password")
        login_button = st.sidebar.button("Login")

        if login_button:
            if authenticate(username, password):
                st.session_state.authentication_status = True
                st.session_state.name = names[usernames.index(username)]
                st.session_state.username = username
                st.sidebar.success(f"Welcome, {st.session_state.name}")
                st.session_state.current_page = "landing_page"
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid username or password.")

# Landing page
def landing_page():
    st.markdown("<h1>Welcome to the Board Evaluation System</h1>", unsafe_allow_html=True)
    st.markdown("<h5>Please proceed with the evaluation by selecting an option below:</h5>", unsafe_allow_html=True)
    
    if st.button("Evaluate the Board"):
        st.session_state.current_page = "board_evaluation"
        st.rerun()

    if st.button("Peer Review"):
        st.session_state.current_page = "peer_review"
        st.rerun()
    
    if st.button("Chairman Review"):
        st.session_state.current_page = "chairman_review"
        st.rerun()

    if st.button("Trust Secretary  Review"):
        st.session_state.current_page = "trust secretary _review"
        st.rerun()

    if st.button("Committee Review"):
        st.session_state.current_page = "committee_review"
        st.rerun()

# Board evaluation page
def board_evaluation():
    criteria = {
        "Strategic Vision and Direction": [
            "How effectively does the board articulate a clear strategic vision for the organization?",
            "To what extent does the board set realistic and achievable strategic goals?",
            "How well does the board monitor and adapt the strategic plan in response to changing circumstances?"
        ],
        "Alignment with Organizational Mission": [
            "How well does the board ensure that the strategic plan aligns with the organization's mission and values?",
            "To what extent does the board consider stakeholder needs and expectations in strategic planning?"
        ],
        "Decision-Making and Implementation": [
            "How effective is the board in making strategic decisions that drive the organization forward?",
            "To what extent does the board ensure that strategic decisions are implemented effectively?",
            "How well does the board evaluate and learn from the outcomes of strategic initiatives?"
        ],
        "Resource Allocation": [
            "How effectively does the board allocate resources (financial, human, and material) to support the strategic plan?",
            "To what extent does the board ensure that resource allocation aligns with strategic priorities?"
        ],
        "Risk Management": [
            "How well does the board identify and manage risks that could impact the strategic plan?",
            "To what extent does the board have contingency plans in place for strategic risks?"
        ],
        "Performance Monitoring and Evaluation": [
            "How effectively does the board monitor the progress of the strategic plan against established benchmarks?",
            "To what extent does the board use performance data to make informed strategic decisions?"
        ],
        "Stakeholder Engagement": [
            "How well does the board engage with key stakeholders (e.g., employees, customers, investors) in the strategic planning process?",
            "To what extent does the board communicate strategic goals and progress to stakeholders?"
        ],
        "Innovation and Adaptability": [
            "How effectively does the board foster a culture of innovation within the organization?",
            "To what extent does the board encourage and support strategic initiatives that involve new ideas and approaches?",
            "How well does the board adapt the strategic plan in response to emerging trends and opportunities?"
        ],
        "Leadership and Governance": [
            "How well does the board provide leadership in driving the strategic direction of the organization?",
            "To what extent does the board demonstrate good governance practices in strategic planning and execution?"
        ],
        "Long-term Sustainability": [
            "How effectively does the board plan for the long-term sustainability and growth of the organization?",
            "To what extent does the board consider environmental, social, and economic factors in strategic planning?"
        ]
    }

    st.markdown("<h5>Please rate the Board on the following aspects on a scale of 1 (Very Poor) to 5 (Excellent).</h5>", unsafe_allow_html=True)

    ratings = st.session_state.ratings_board
    for section, questions in criteria.items():
        st.subheader(section)
        for question in questions:
            st.write(question)
            rating = st.radio(
                label="Select your rating",
                options=[1, 2, 3, 4, 5],
                index=ratings.get(question, 0) - 1 if question in ratings else 0,
                key=f"Board_{question}_rating",
                horizontal=True,
            )
            if rating:
                ratings[question] = rating

    st.write("Here is a summary of your ratings:")
    for question, rating in ratings.items():
        st.write(f"{question}: {rating}")

    if ratings:
        average_rating = sum(ratings.values()) / len(ratings)
        st.write(f"Overall Average Rating: {average_rating:.2f}")

        st.header("Ratings Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(list(ratings.keys()), list(ratings.values()), color='#66c2ff')
        ax.set_xlabel('Ratings')
        ax.set_title("Board Evaluation Ratings")
        plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
        st.pyplot(fig)

    st.header("Additional Feedback")
    additional_feedback = st.text_area("Please provide any additional comments or suggestions:", key="board_feedback")

    if len(ratings) == sum(len(questions) for questions in criteria.values()):
        if st.button("Submit Feedback"):
            feedback_data = pd.DataFrame([
                {"Question": question, "Rating": rating}
                for question, rating in ratings.items()
            ])
            feedback_data["Username"] = st.session_state.username
            feedback_data["Additional Feedback"] = additional_feedback
            feedback_data.to_csv(f"{st.session_state.username}_board_feedback.csv", index=False)
            st.write("Thank you for your feedback! Your response has been saved.")
            st.session_state.current_page = "landing_page"
            st.experimental_rerun()
    else:
        st.error("Please rate all aspects before submitting your feedback.")

# Peer review page
def peer_review():
    criteria = {
        "Leadership": [
            "Ability to lead and influence the board effectively."
        ],
        "Collaboration": [
            "Effectiveness in working with other board members."
        ],
        "Strategic Thinking": [
            "Contribution to strategic planning and oversight."
        ],
        "Communication": [
            "Effectiveness in communication with the board and stakeholders."
        ],
        "Decision Making": [
            "Ability to make informed and effective decisions."
        ]
    }

    st.markdown("<h5>Please rate your peers on the following aspects on a scale of 1 (Very Poor) to 5 (Excellent).</h5>", unsafe_allow_html=True)

    ratings = st.session_state.ratings_peer
    for member in names:
        if member != st.session_state.name:
            st.header(f"Evaluate {member}")
            for section, questions in criteria.items():
                st.subheader(section)
                for question in questions:
                    st.write(question)
                    rating = st.radio(
                        label="Select your rating",
                        options=[1, 2, 3, 4, 5],
                        index=ratings.get(member, {}).get(question, 0) - 1 if member in ratings and question in ratings[member] else 0,
                        key=f"{member}_{question}_rating",
                        horizontal=True,
                    )
                    if rating:
                        if member not in ratings:
                            ratings[member] = {}
                        ratings[member][question] = rating

    st.write("Here is a summary of your ratings:")

    for member, member_ratings in ratings.items():
        st.subheader(f"Ratings for {member}")
        for question, rating in member_ratings.items():
            st.write(f"{question}: {rating}")

    if ratings:
        for member, member_ratings in ratings.items():
            average_rating = sum(member_ratings.values()) / len(member_ratings)
            st.write(f"Overall Average Rating for {member}: {average_rating:.2f}")

            st.header(f"Ratings Distribution for {member}")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(list(member_ratings.keys()), list(member_ratings.values()), color='#66c2ff')
            ax.set_xlabel('Ratings')
            ax.set_title(f"Peer Review Ratings for {member}")
            plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
            st.pyplot(fig)

    st.header("Additional Feedback")
    additional_feedback = st.text_area("Please provide any additional comments or suggestions about your peers:", key="peer_feedback")

    if all(len(member_ratings) == sum(len(questions) for questions in criteria.values()) for member_ratings in ratings.values()):
        if st.button("Submit Feedback"):
            feedback_data = pd.DataFrame([
                {"Member": member, "Question": question, "Rating": rating}
                for member, member_ratings in ratings.items()
                for question, rating in member_ratings.items()
            ])
            feedback_data["Username"] = st.session_state.username
            feedback_data["Additional Feedback"] = additional_feedback
            feedback_data.to_csv(f"{st.session_state.username}_peer_feedback.csv", index=False)
            st.write("Thank you for your feedback! Your response has been saved.")
            st.session_state.current_page = "landing_page"
            st.experimental_rerun()
    else:
        st.error("Please rate all aspects for all peers before submitting your feedback.")

# Chairman review page
def chairman_review():
    criteria = {
        "Leadership": [
            "Visionary leadership and strategic direction.",
            "Effectiveness in chairing meetings."
        ],
        "Governance": [
            "Ensuring good governance practices.",
            "Compliance with policies and regulations."
        ],
        "Communication": [
            "Clear and effective communication with board members.",
            "Representing the board to stakeholders."
        ]
    }

    st.markdown("<h5>Please rate the Chairman on the following aspects on a scale of 1 (Very Poor) to 5 (Excellent).</h5>", unsafe_allow_html=True)

    ratings = st.session_state.ratings_chairman
    for section, questions in criteria.items():
        st.subheader(section)
        for question in questions:
            st.write(question)
            rating = st.radio(
                label="Select your rating",
                options=[1, 2, 3, 4, 5],
                index=ratings.get(question, 0) - 1 if question in ratings else 0,
                key=f"Chairman_{question}_rating",
                horizontal=True,
            )
            if rating:
                ratings[question] = rating

    st.write("Here is a summary of your ratings:")
    for question, rating in ratings.items():
        st.write(f"{question}: {rating}")

    if ratings:
        average_rating = sum(ratings.values()) / len(ratings)
        st.write(f"Overall Average Rating: {average_rating:.2f}")

        st.header("Ratings Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(list(ratings.keys()), list(ratings.values()), color='#66c2ff')
        ax.set_xlabel('Ratings')
        ax.set_title("Chairman Evaluation Ratings")
        plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
        st.pyplot(fig)

    st.header("Additional Feedback")
    additional_feedback = st.text_area("Please provide any additional comments or suggestions:", key="chairman_feedback")

    if len(ratings) == sum(len(questions) for questions in criteria.values()):
        if st.button("Submit Feedback"):
            feedback_data = pd.DataFrame([
                {"Question": question, "Rating": rating}
                for question, rating in ratings.items()
            ])
            feedback_data["Username"] = st.session_state.username
            feedback_data["Additional Feedback"] = additional_feedback
            feedback_data.to_csv(f"{st.session_state.username}_chairman_feedback.csv", index=False)
            st.write("Thank you for your feedback! Your response has been saved.")
            st.session_state.current_page = "landing_page"
            st.experimental_rerun()
    else:
        st.error("Please rate all aspects before submitting your feedback.")

# Trustee review page
def trustee_review():
    criteria = {
        "Organization and Management Skills": [
                "How effectively does the Trustee Secretary manage and organize board meetings?",
            "To what extent does the Trustee Secretary ensure that board members receive all necessary documents and information in a timely manner?",
            "How well does the Trustee Secretary maintain and organize board records and documentation?"
            ],
        "Communication":[ 
            "How effectively does the Trustee Secretary communicate with board members, ensuring clarity and completeness of information?",
            "To what extent does the Trustee Secretary facilitate communication between the board and other stakeholders?",
            "How well does the Trustee Secretary address and resolve any communication issues that arise?"
            ],

        "Compliance and Governance":[
            "How effectively does the Trustee Secretary ensure that the board adheres to legal and regulatory requirements?",
            "To what extent does the Trustee Secretary support the board in maintaining good governance practices?",
            "How well does the Trustee Secretary stay informed about changes in laws and regulations that may impact the board?"
                    ],

        "Meeting Facilitation":[ 
                                "How effectively does the Trustee Secretary facilitate the smooth running of board meetings?",
            "To what extent does the Trustee Secretary ensure that meeting agendas are clear and comprehensive?",
            "How well does the Trustee Secretary handle minutes and action items from meetings?"
                            ],
    
        "Support to the Board":[
            "How effectively does the Trustee Secretary support the board in carrying out its responsibilities?",
            "To what extent does the Trustee Secretary provide useful and timely advice to board members?",
        " How well does the Trustee Secretary anticipate and respond to the needs of the board?"
        ]
   
    }

    st.markdown("<h5>Please rate the Trustees on the following aspects on a scale of 1 (Very Poor) to 5 (Excellent).</h5>", unsafe_allow_html=True)

    ratings = st.session_state.ratings_trustee
    for section, questions in criteria.items():
        st.subheader(section)
        for question in questions:
            st.write(question)
            rating = st.radio(
                label="Select your rating",
                options=[1, 2, 3, 4, 5],
                index=ratings.get(question, 0) - 1 if question in ratings else 0,
                key=f"Trustee_{question}_rating",
                horizontal=True,
            )
            if rating:
                ratings[question] = rating

    st.write("Here is a summary of your ratings:")
    for question, rating in ratings.items():
        st.write(f"{question}: {rating}")

    if ratings:
        average_rating = sum(ratings.values()) / len(ratings)
        st.write(f"Overall Average Rating: {average_rating:.2f}")

        st.header("Ratings Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(list(ratings.keys()), list(ratings.values()), color='#66c2ff')
        ax.set_xlabel('Ratings')
        ax.set_title("Trustee Evaluation Ratings")
        plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
        st.pyplot(fig)

    st.header("Additional Feedback")
    additional_feedback = st.text_area("Please provide any additional comments or suggestions:", key="trustee_feedback")

    if len(ratings) == sum(len(questions) for questions in criteria.values()):
        if st.button("Submit Feedback"):
            feedback_data = pd.DataFrame([
                {"Question": question, "Rating": rating}
                for question, rating in ratings.items()
            ])
            feedback_data["Username"] = st.session_state.username
            feedback_data["Additional Feedback"] = additional_feedback
            feedback_data.to_csv(f"{st.session_state.username}_trustee_feedback.csv", index=False)
            st.write("Thank you for your feedback! Your response has been saved.")
            st.session_state.current_page = "landing_page"
            st.experimental_rerun()
    else:
        st.error("Please rate all aspects before submitting your feedback.")

# Committee review page
def committee_review():
    committees = {
        "Audit & Risk Management Committee": [
            "Effectiveness in overseeing financial reporting.",
            "Management of risk and compliance."
        ],
        "Investment and Reporting Committee": [
            "Strategic oversight of investments.",
            "Transparency in reporting."
        ],
        "Welfare and Administration Committee": [
            "Enhancement of member welfare.",
            "Efficiency in administrative processes."
        ]
    }

    st.markdown("<h5>Please rate the committees on the following aspects on a scale of 1 (Very Poor) to 5 (Excellent).</h5>", unsafe_allow_html=True)

    ratings = st.session_state.ratings_committee
    for committee, questions in committees.items():
        st.header(committee)
        for question in questions:
            st.write(question)
            rating = st.radio(
                label="Select your rating",
                options=[1, 2, 3, 4, 5],
                index=ratings.get(committee, {}).get(question, 0) - 1 if committee in ratings and question in ratings[committee] else 0,
                key=f"{committee}_{question}_rating",
                horizontal=True,
            )
            if rating:
                if committee not in ratings:
                    ratings[committee] = {}
                ratings[committee][question] = rating

    st.write("Here is a summary of your ratings:")
    for committee, committee_ratings in ratings.items():
        st.subheader(f"Ratings for {committee}")
        for question, rating in committee_ratings.items():
            st.write(f"{question}: {rating}")

    if ratings:
        for committee, committee_ratings in ratings.items():
            average_rating = sum(committee_ratings.values()) / len(committee_ratings)
            st.write(f"Overall Average Rating for {committee}: {average_rating:.2f}")

            st.header(f"Ratings Distribution for {committee}")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(list(committee_ratings.keys()), list(committee_ratings.values()), color='#66c2ff')
            ax.set_xlabel('Ratings')
            ax.set_title(f"Committee Review Ratings for {committee}")
            plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
            st.pyplot(fig)

    st.header("Additional Feedback")
    additional_feedback = st.text_area("Please provide any additional comments or suggestions about the committees:", key="committee_feedback")

    if all(len(committee_ratings) == len(questions) for committee, questions in committees.items() for committee_ratings in ratings.values() if committee == committee_ratings):
        if st.button("Submit Feedback"):
            feedback_data = pd.DataFrame([
                {"Committee": committee, "Question": question, "Rating": rating}
                for committee, committee_ratings in ratings.items()
                for question, rating in committee_ratings.items()
            ])
            feedback_data["Username"] = st.session_state.username
            feedback_data["Additional Feedback"] = additional_feedback
            feedback_data.to_csv(f"{st.session_state.username}_committee_feedback.csv", index=False)
            st.write("Thank you for your feedback! Your response has been saved.")
            st.session_state.current_page = "landing_page"
            st.experimental_rerun()
    else:
        st.error("Please rate all aspects for all committees before submitting your feedback.")

# Display the appropriate page based on session state
def display_page():
    if st.session_state.current_page == "login_page":
        login_page()
    elif st.session_state.current_page == "landing_page":
        landing_page()
    elif st.session_state.current_page == "board_evaluation":
        board_evaluation()
    elif st.session_state.current_page == "peer_review":
        peer_review()
    elif st.session_state.current_page == "chairman_review":
        chairman_review()
    elif st.session_state.current_page == "trustee_review":
        trustee_review()
    elif st.session_state.current_page == "committee_review":
        committee_review()

# Main app execution
if __name__ == "__main__":
    display_page()
