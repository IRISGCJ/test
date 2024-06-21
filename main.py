import streamlit as st
import folium
from streamlit_folium import st_folium
import openrouteservice

# 设置OpenRouteService API密钥
ORS_API_KEY = '5b3ce3597851110001cf6248ec4432c73f4f4735a30df115efb8e6bc'

# 获取路线规划
def get_directions(client, start_coords, end_coords):
    try:
        routes = client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson'
        )
        return routes
    except Exception as e:
        st.error(f'获取路线失败: {e}')
        return None

# 输入起点和终点的经纬度
st.title('路线规划器')
start_lat = st.number_input('起点纬度', value=39.9042)  # 北京的纬度
start_lon = st.number_input('起点经度', value=116.4074)  # 北京的经度
end_lat = st.number_input('终点纬度', value=31.2304)    # 上海的纬度
end_lon = st.number_input('终点经度', value=121.4737)   # 上海的经度

# 创建OpenRouteService客户端
client = openrouteservice.Client(key=ORS_API_KEY)

# 获取路线
start_coords = (start_lon, start_lat)
end_coords = (end_lon, end_lat)
route = get_directions(client, start_coords, end_coords)

# 创建Folium地图
map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
m = folium.Map(location=map_center, zoom_start=5)

# 添加起点和终点标记
folium.Marker([start_lat, start_lon], tooltip='起点', icon=folium.Icon(color='green')).add_to(m)
folium.Marker([end_lat, end_lon], tooltip='终点', icon=folium.Icon(color='red')).add_to(m)

# 绘制路线
if route:
    folium.GeoJson(route, name='路线').add_to(m)

# 显示Folium地图
st_folium(m, width=700, height=500)
