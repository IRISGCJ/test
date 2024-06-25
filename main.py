import streamlit as st
import openrouteservice
from streamlit_folium import st_folium
import folium

# 创建OpenRouteService客户端
client = openrouteservice.Client(key='5b3ce3597851110001cf6248ec4432c73f4f4735a30df115efb8e6bc')

# 使用缓存来存储路由数据
@st.cache(ttl=3600)
def get_directions(client, start_coords, end_coords):
    try:
        routes = client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson'
        )
        return routes
    except openrouteservice.exceptions.ApiError as e:
        st.error(f"API请求错误: {e}")
        return None
    except openrouteservice.exceptions.HTTPError as e:
        st.error(f"HTTP错误: {e}")
        return None
    except Exception as e:
        st.error(f"未知错误: {e}")
        return None

# 用户输入起点和终点
start_coords = (-0.1061000, 51.5567000)
end_coords = (-1.8847000, 52.5092000)

# 获取路线数据
routes = get_directions(client, start_coords, end_coords)

# 初始化地图
m = folium.Map(location=[(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2], zoom_start=7)

# 在地图上添加路线
if routes:
    folium.GeoJson(routes).add_to(m)
else:
    st.error("无法获取路线数据")

# 在Streamlit应用中显示地图
st_folium(m, width=700, height=500)
