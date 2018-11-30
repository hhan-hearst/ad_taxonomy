# Beauty site scraper #
This is a tool for fetching Beauty Taxnomy information from Sephora.

### Libraries used:

The project runs on Python 2.7.

	1. Scrapy
	3. scrapy-fake-useragent for rotating browser headers.
### Run the job(Save output into sephora.json):
	scrapy crawl sephora -o sephora.json
### About output:
	There are about 16,000 products with category, subcategory, price, description, etc..

# Generate the model

open up the notebook and run the code block sequentially:

`ipython notebook`


