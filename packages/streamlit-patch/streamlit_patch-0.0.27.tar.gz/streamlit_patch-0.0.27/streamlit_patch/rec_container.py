import streamlit as st

from .db_connector import search_by_product_name


class RecContainer:
  
    @staticmethod
    def init(db_path, CCB_path):
        RecContainer.CCB_path = CCB_path
        RecContainer.db_path = db_path
    def __init__(self):
        rec_container = st.container()
        with rec_container.popover("💡",use_container_width=True).container(height=350):
            data = ["华夏策略", "华安安康灵活配置A", "易增回报A"]
            for item in data:
                with st.container():
                    col1, col2, col3 = st.columns([2,3,4])
                    col1.markdown(item)
                    chart_data = search_by_product_name(
                        RecContainer.CCB_path,
                        RecContainer.db_path,
                        item,
                    )
                    col2.line_chart(
                        chart_data,
                        y=["unit_net_worth", "acc_net_worth"],
                        x="date",
                        x_label=item,
                        y_label="盈利趋势",
                        height=160,
                        width=400,
                        use_container_width=False,
                    )
                    col3.checkbox("Submit")
                    st.divider()
        rec_container.float("position: fixed; bottom: 150px; right: 50px; z-index: 9999; width: 4rem; height: 2rem;")
