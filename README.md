**Follow Harpo's epicurean journey via snippets of his autobiography and the NYPL menu collection!**

# About  
*Harpo Eats!* is a program to computer-generate a novel of ~50,000 words, in the spirit of [NaNoGenMo](https://nanogenmo.github.io). Taking excerpts to do with food from Harpo Marx's autobiography Harpo Speaks! (Marx, Harpo. *Harpo Speaks!* New York: Limelight, 1985.), it arbitrarily replaces mentions of dishes, restaurants and eating places, and meal and dish costs—in various period-appropriate formats—with corresponding items arbitrarily selected from the New York Public Library's collection of menus ([What's on the Menu?](http://menus.nypl.org)). The number of dishes Harpo orders and consumes increase exponentially as we follow the very abridged narrative of his life (in sequential order). The program further makes use of [OpenAI's DALL·E 2](https://openai.com/dall-e-2/) to computer generate the originally lacking illustrations. By exponentially increasing Harpo's food orders and food consumption (and presumably digestive abilities), *Harpo Eats!* thereby increases the already international, translingual, and transcultural nature of food to match the supremely international, translingual, and transcultural nature of the best Marx brother.  

# To Run  
*Harpo Eats!* requires a few python packages, most you will already have installed. These two maybe not: `openai`, and `reportlab`. It also runs on python 3. To install these two packages:    
    pip3 install openai  
    pip3 install reportlab  
Lastly, in the directory housing the other two necessary files from this repo (`harpos_menu.pkl`, `excerpts.txt`), run `python3 halff_wmd_4.0.py`. It will ask you for a OpenAI organization code and API token, [which you can get here](https://beta.openai.com/account/api-keys), after making an account or signing in. The program will run and produce a PDF of *Harpo Eats!*.
