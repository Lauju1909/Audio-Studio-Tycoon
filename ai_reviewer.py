import random

class ai_reviewer:
    @staticmethod
    def generate_review(game_state, game, score):
        """
        Generates a review text based on game performance and topic/genre compatibility.
        """
        # Get topic and genre names from translations
        topic_name = game_state.get_text(game.topic)
        genre_name = game_state.get_text(game.genre)
        
        # Determine performance category
        is_masterpiece = score >= 9.0
        is_good = score >= 7.0
        is_average = score >= 5.0
        is_bad = score < 5.0
        
        # Select components
        intro_keys = ['review_intro_1', 'review_intro_2', 'review_intro_3', 'review_intro_4', 'review_intro_5']
        prefix = game_state.get_text('review_prefix', default="Review: ")
        
        # Intro
        selected_intro = random.choice(intro_keys)
        intro = game_state.get_text(selected_intro, 
                                    company=game_state.company_name or "Unknown Studio", 
                                    game=game.name or "Untitled Game")
        
        # Body based on quality and compatibility
        if is_masterpiece:
            body_keys = ['review_pos_1', 'review_pos_3']
            body = game_state.get_text(random.choice(body_keys), topic=topic_name, genre=genre_name)
            gameplay = game_state.get_text('review_good_gameplay')
            conclusion = game_state.get_text('review_concl_1')
        elif is_good:
            body_keys = ['review_pos_3', 'review_pos_2']
            body = game_state.get_text(random.choice(body_keys), topic=topic_name, genre=genre_name)
            gameplay = game_state.get_text('review_good_gameplay')
            conclusion = game_state.get_text('review_concl_2')
        elif is_average:
            body = game_state.get_text('review_pos_2', genre=genre_name)
            gameplay = game_state.get_text('review_avg_gameplay')
            conclusion = game_state.get_text('review_concl_2')
        else:
            # Bad
            body_keys = ['review_neg_1', 'review_neg_2', 'review_neg_3']
            body = game_state.get_text(random.choice(body_keys), topic=topic_name, genre=genre_name)
            gameplay = game_state.get_text('review_bad_gameplay')
            conclusion = game_state.get_text('review_concl_3')
            
        # Combine
        review = f"{prefix}{intro} {body} {gameplay} {conclusion}"
        return review

