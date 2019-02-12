# Chuck Norris sitemap cloudfront

This project is intended for use as a lambda@edge function that will check if resources in the website sitemap are updated from cloudfront and in this case if sitemap must be updated too.

## Objective

The main objective is to put large cache (even forever) times for sitemaps in order to update them from cloudfront only when they are requested and they are not updated at all