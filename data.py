import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_screener_in(symbol):
    try:
        
        url = f"https://www.screener.in/company/{symbol}/consolidated"

        
        response = requests.get(url)

        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')

            
            company_name_element = soup.find('h1', class_='shrink-text')
            if company_name_element:
                company_name = company_name_element.text.strip()
                st.write(f"Company Name: {company_name}")
            
            company_ratios = soup.find('div', class_='company-ratios')

            if company_ratios:
                
                top_ratios_ul = company_ratios.find('ul', id='top-ratios')
                if top_ratios_ul:
                    
                    stock_pe_element = top_ratios_ul.find('li', class_='flex flex-space-between', string=' Stock P/E ')
                    if stock_pe_element:
                        
                        stock_pe_value = stock_pe_element.find('span', class_='number').text
                        print(f"Stock P/E Value: {stock_pe_value}")
                    else:
                        print("Stock P/E not found.")
                else:
                    print("Top ratios ul not found.")
            else:
                print("Company ratios div not found.")
            
            

        else:
            st.error("Failed to fetch data. Check the company symbol and try again.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

def home_page():
    st.title("Home Page")
    st.write("This site provides interactive tools to valuate and analyze stocks through Reverse DCF model. Check the navigation bar for more.")

def DCF_Valuation():
    st.title("VALUING CONSISTENT COMPOUNDERS")
    st.write("Hi there!")
    st.write("This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.")
    st.write("We then compare this with current PE of the stock to calculate degree of overvaluation.")
    symbol = st.text_input("Enter NSE/BSE symbol")
    if st.button("Scrape Data"):
        if symbol:
            scrape_screener_in(symbol)
        else:
            st.warning("Please enter a symbol to fetch data.")

def main():
    st.sidebar.title("REVERSE DCF")
    page_options = ["Home", "DCF Valuation"]
    selected_page = st.sidebar.radio("Go to", page_options)

    if selected_page == "Home":
        home_page()
    elif selected_page == "DCF Valuation":
        DCF_Valuation()

if __name__ == "__main__":
    main()
