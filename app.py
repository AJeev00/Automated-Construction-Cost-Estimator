import streamlit as st
import pandas as pd
from io import BytesIO
st.set_page_config(page_title="BuildQuant | Cost Estimator",page_icon="🧮",layout="wide")
st.title("BuildQuant")
st.caption("Preliminary Building Quantity & Cost Estimator | Editable assumptions")
st.warning("Educational estimating prototype. Rates and quantities must be checked against drawings, specifications, local SOR and site conditions.")
st.sidebar.header("Project assumptions")
length=st.sidebar.number_input("Building length (m)",min_value=1.0,value=12.0,step=.5)
width=st.sidebar.number_input("Building width (m)",min_value=1.0,value=9.0,step=.5)
wall=st.sidebar.number_input("External wall thickness (m)",min_value=.1,max_value=.5,value=.23,step=.01)
height=st.sidebar.number_input("Wall height (m)",min_value=2.0,max_value=6.0,value=3.0,step=.1)
openings=st.sidebar.slider("Openings deduction (%)",0,40,15)
foundation_width=st.sidebar.number_input("Foundation trench width (m)",min_value=.3,max_value=2.0,value=.9,step=.05)
foundation_depth=st.sidebar.number_input("Foundation depth (m)",min_value=.3,max_value=3.0,value=1.0,step=.1)
perimeter=2*(length+width)
exc=perimeter*foundation_width*foundation_depth
pcc=perimeter*foundation_width*.1
wall_vol=perimeter*wall*height*(1-openings/100)
dpc=perimeter*wall
floor=length*width
st.subheader("Quantity take-off")
items=[
("Earthwork excavation","m³",exc,650),
("PCC bed in foundation","m³",pcc,6500),
("Brickwork in superstructure","m³",wall_vol,8500),
("DPC (assumed 25 mm thick)","m²",dpc,450),
("Floor finish","m²",floor,950),
]
rates={}
for name,unit,q,default in items:
    rates[name]=default
with st.expander("Edit indicative unit rates",expanded=True):
    cols=st.columns(3)
    for i,(name,unit,q,default) in enumerate(items):
        rates[name]=cols[i%3].number_input(f"{name} (₹/{unit})",min_value=0,value=default,step=50,key=name)
rows=[]
for name,unit,q,_ in items:
    rows.append({"Item":name,"Unit":unit,"Quantity":round(q,3),"Rate (₹)":rates[name],"Amount (₹)":round(q*rates[name],2)})
df=pd.DataFrame(rows)
subtotal=df["Amount (₹)"].sum()
contingency=st.slider("Contingency (%)",0,20,5)
tax=st.slider("Additional allowance (%)",0,30,0)
total=subtotal*(1+contingency/100)*(1+tax/100)
a,b,c=st.columns(3)
a.metric("Built-up floor area",f"{floor:.1f} m²")
b.metric("Base estimate",f"₹{subtotal:,.0f}")
c.metric("Indicative total",f"₹{total:,.0f}")
st.dataframe(df,use_container_width=True,hide_index=True)
st.subheader("Cost composition")
st.bar_chart(df.set_index("Item")["Amount (₹)"])
summary=pd.DataFrame([{"Description":"Subtotal","Amount (₹)":subtotal},{"Description":"Contingency","Amount (₹)":subtotal*contingency/100},{"Description":"Additional allowance","Amount (₹)":subtotal*(1+contingency/100)*tax/100},{"Description":"Indicative total","Amount (₹)":total}])
st.dataframe(summary,use_container_width=True,hide_index=True)
csv=df.to_csv(index=False).encode()
st.download_button("Download BOQ (CSV)",csv,"preliminary_boq.csv","text/csv")
buf=BytesIO()
with pd.ExcelWriter(buf,engine="openpyxl") as writer:
    df.to_excel(writer,index=False,sheet_name="BOQ")
    summary.to_excel(writer,index=False,sheet_name="Summary")
st.download_button("Download estimate (Excel)",buf.getvalue(),"preliminary_estimate.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.caption("Simplified geometry: rectangular perimeter-based quantities. Internal walls, junctions, lintels, reinforcement, staircases, services, wastage and detailed specifications are excluded.")
