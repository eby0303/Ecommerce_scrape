import streamlit as st
import pandas as pd
from scrape import scrape_data


def download_csv(amazon_data, flipkart_data):
    # Create DataFrames from the scraped data
    if amazon_data:
        amazon_df = pd.DataFrame(amazon_data)
    else:
        amazon_df = pd.DataFrame()

    if flipkart_data:
        flipkart_df = pd.DataFrame(flipkart_data)
    else:
        flipkart_df = pd.DataFrame()

    # Save DataFrames to CSV files
    if not amazon_df.empty:
        amazon_csv = amazon_df.to_csv(index=False)
        st.download_button(label="Download Amazon Data", data=amazon_csv, file_name='amazon_data.csv', mime='text/csv')

    if not flipkart_df.empty:
        flipkart_csv = flipkart_df.to_csv(index=False)
        st.download_button(label="Download Flipkart Data", data=flipkart_csv, file_name='flipkart_data.csv', mime='text/csv')



def display_table(results):
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(results)

    # Display the DataFrame
    st.dataframe(df)
    
    
    
def main():
    st.title('Product Information Scraper')

    #Input field for entering the product name
    product = st.text_input('Enter the Product')

    if product:
        # Generate URLs
        amazon_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
        flipkart_url = f"https://www.flipkart.com/search?q={product.replace(' ', '+')}"

        st.markdown(f"Generated Amazon URL: [Link]({amazon_url})")
        st.markdown(f"Generated Flipkart URL: [Link]({flipkart_url})")

        #Input wanted list items for Amazon
        st.write("Visit the Amazon URL and copy the information you want to scrape.")
        amazon_wanted_list_input = st.text_input('Enter the Amazon wanted list items (separated by hashtag)')

        #Input wanted list items for Flipkart
        st.write("Visit the Flipkart URL and copy the information you want to scrape.")
        flipkart_wanted_list_input = st.text_input('Enter the Flipkart wanted list items (separated by hashtag)')

        if st.button('Scrape Data'):
            amazon_wanted_list = [item.strip() for item in amazon_wanted_list_input.split('#')]
            flipkart_wanted_list = [item.strip() for item in flipkart_wanted_list_input.split('#')]

            amazon_results = scrape_data(amazon_url, amazon_wanted_list)
            flipkart_results = scrape_data(flipkart_url, flipkart_wanted_list)

            # Display the results in a table
            if amazon_results or flipkart_results:
                st.write("Scraped Data:")
                if amazon_results:
                    st.subheader("Amazon:")
                    display_table(amazon_results)
                
                if flipkart_results:
                    st.subheader("Flipkart:")
                    display_table(flipkart_results)

                #Download button for CSV
                if st.button('Download CSV'):
                    download_csv(amazon_results, flipkart_results)

            else:
                st.write("No data found or invalid wanted list items.")

if __name__ == "__main__":
    main()
