This project is developed to automatically detect changes made to the official Telegram sites. This is necessary for anticipating threat within messages

Link crawling runs as often as possible. Starts crawling from the home page of the site. Detects relative and absolute sub links and recursively repeats the operation. Writes a list of unique links for future content comparison. Additionally, there is the ability to add links by hand to help the script find more hidden (links to which no one refers) links. To manage exceptions, there is a system of rules for the link crawler.

Content crawling is launched as often as possible and uses the existing list of links collected in step 1. Going through the base it gets contains and builds a system of subfolders and files. Removes all dynamic content from files.

Using of GitHub Actions. Works without own servers. You can just fork this repository and own tracker system by yourself. Workflows launch scripts and commit changes. All file changes are tracked by the GIT and beautifully displayed on the GitHub. GitHub Actions should be built correctly only if there are changes on the Telegram website. Otherwise, the workflow should fail. If build was successful, we can send notifications to Telegram channel and so on.
