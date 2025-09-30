import streamlit as st
import pandas as pd
from modules.navbar import navbar

from visuals.histogram import histogram
from visuals.donut import donut
from visuals.review_score_barplot import review_score_barplot
from visuals.review_wordcloud import review_wordcloud


def review_scores():
    navbar()

    st.set_page_config(
        page_title="Olist Analysis",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    df = cached_df
    st.subheader("Review Score Distribution")

    left_dist, gap_dist, right_dist = st.columns([5, 1, 6], vertical_alignment="top")
    with left_dist:
        score_donut = donut(df, 'review_score')
        st.plotly_chart(score_donut)
    with right_dist:
        score_hist = histogram(df, 'review_score', 'Review Score', 'Number of Reviews', 'All Reviews')
        st.plotly_chart(score_hist)

    left_dist_comment, gap_2, right_dist_comment = st.columns([5, 1, 6], vertical_alignment="top")
    with left_dist_comment:
        st.markdown("The analysis of missing review comments reveals that:")
        st.markdown("""- Negative reviews (1-2 stars) are more likely to contain
                    written feedback, while higher ratings (4-5 stars) often
                    lack text comments.""")
        st.markdown("""- This suggests that dissatisfied customers tend to provide
                    detailed feedback, whereas satisfied customers
                    typically leave only a rating.""")
        st.markdown("""- Finally, the comments from the negative reviews can be
                    analyzed to identify key areas for improvement.""")
    with right_dist_comment:
        comment_score_dist = review_score_barplot(df, 'Only Reviews with Comments')
        st.plotly_chart(comment_score_dist)

    if st.checkbox("**:blue-background[Show Word Cloud of Negative Review Comments]**"):
        only_neg_df = df[df['review_score'] < 4.0].reset_index(drop=True)
        comment_wordcloud = review_wordcloud(only_neg_df)
        st.pyplot(comment_wordcloud)

        st.markdown("The most used words and their translations are:")

        most_used_words = pd.DataFrame(
            {
                "Portuguese": ["o produto chegou", "foi entregue", "nao recebi",
                            "estou aguardando", "produto veio", "ainda nao"],
                "English": ["the product arrived", "was delivered", "I did not receive it",
                            "I am waiting", "product came", "not yet"],
            }
        )

        s1 = dict(selector='th', props=[('text-align', 'center')])
        s2 = dict(selector='td', props=[('text-align', 'center')])
        table = most_used_words.style.set_table_styles([s1,s2]).hide(axis=0).to_html()
        st.write(f'{table}', unsafe_allow_html=True)

        st.markdown("""As seen, most negative comments include words related to
                    product delivery and timing. Therefore, the next step
                    will be to analyze delivery times.""")

if __name__ == '__main__':
    if "data" in st.session_state:
        cached_df = st.session_state["data"]
        review_scores()
    else:
        st.switch_page('olistAnalysis.py')
