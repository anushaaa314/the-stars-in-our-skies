# The Stars In Our Skies
A data science project that maps out different qualaties about stars in our universe.

## Message for Snowglobe reviewer!!!!
Hi! I saw the message you left stating I have 11 hours of work not in the repo. If you read below, you will see that I was working on one feature of this program for a long time, but it didn't end up working well, so I deleted it's files. This was my first project where I learned a little bit on how to commit, so I was commiting, but not very regularly. Thus, I didn't really know what to do when I read the message you left since I had deleted the files from the program (though I did keep the code) and did not have a commit I could go back to with the files I spent much of my time on. So, I just created new files, titled them the same name as before, and pasted in the code I had kept, since I don't know how to get the original files back. The tree now shows all of the files I have ever coded for this project, though many are not in use for the final shipped web page. I am very new to using git and commiting, so I am sorry this is not ideal! If you have any questions or confusions, please email me (email: sawhneyanusha@gmail.com), message me on the slack, or honestly, you can just count the hours that I have proper commited files on. Thank you so much!!!

The dataset is from the **Gaia Data Release 3** catalog and includes the distance, speed/direction of movement, color, and temperature of **50,000 stars**
It is built with a python backend and Flask, HTML, and CSS for the frontend. 

I used Python, HTML, and CSS. Within python, I used the following libraries: Flask, pathlib, matplotlib, pandas, numpy, astropy, requests, io, and astroquery

## Something I learned from and changed in the project
In the beginning, I actually wanted to use a clustering ML algorithm to indentify groups of stars that move together. However, the two algorithms I tested (DBSCAN and HDBSCAN) both had a tendency to do something called the chaining effect. One cluster would easily connect to another because of two of their ends being extremely close together, even though they were very much apart. Because the dataset was so huge, almost every star had a neighbor and it was really hard to cluster. So instead, I created a map that color codes stars based on the direction they move in. That map also shows cluster of stars moving in similar directions without the clustering confusion. Making the second map for the direction inspired me to create three more for the speed, color, and temperature of the stars, and that led to my final project!



How the direction graph colors clusters


<img width="1892" height="857" alt="image" src="https://github.com/user-attachments/assets/97939b76-af65-446d-9261-4c7b3cce0639" />


## Astronomy understanding and math
I also struggled with some of the mathematical concepts related to calculating the components of this project, but through a lot of googling I eventually understood. Below are some images that really helped me. You can reference these while viewing the project:

Parallax

<img width="469" height="305" alt="parallax_calc" src="https://github.com/user-attachments/assets/04594828-78e3-485d-bfbb-e1371f30284a" />

Right Ascension and Declination

<img width="583" height="472" alt="post-8131-1407381223903_thumb" src="https://github.com/user-attachments/assets/598d1957-5202-436d-9c06-3a5b7c55d143" />

This one kind of helped with Angular Speed 
<img width="1486" height="850" alt="image" src="https://github.com/user-attachments/assets/161c1a23-70d7-40fd-8fcd-e7f168d6007a" />


and so did this google search...

"To calculate total angular speed (also called total proper motion, \(\mu \)) from the proper motion in right ascension (\(\mu _{\alpha }^{*}\) or pmra) and declination (\(\mu _{\delta }\) or pmdec), you use the Pythagorean theorem.
\(\mu =\sqrt{\mu _{\alpha }^{*2}+\mu _{\delta }^{2}}\)

Step-by-Step Calculation

1. Verify pmra is already corrected: In modern astronomical catalogs (like Gaia or Hipparcos), pmra is typically given as \(\mu_{\alpha}^* = \mu_{\alpha} \cos\delta\). Check your dataset documentation. If it is already corrected, proceed directly to step 3.
2. Apply the cosine correction (if uncorrected): If your pmra value is just raw \(\mu _{\alpha }\), you must multiply it by the cosine of the star's declination (\(\delta \)) to account for the convergence of right ascension lines at the poles:
\(\mu _{\alpha }^{*}=\text{pmra}\times \cos (\text{dec})\)
3. Square both components: Calculate \((\mu_{\alpha}^*)^2\) and \((\mu_{\delta})^2\).
4. Sum and square root: Add the two squared values together and take the square root of the sum.

🐍 Python Example

python
import numpy as np

pmra_corrected = -3.45  # Already includes the cos(dec) factor
pmdec = 5.12

total_proper_motion = np.sqrt(pmra_corrected**2 + pmdec**2)

print(f"Total angular speed: {total_proper_motion:.3f} mas/yr")
Use code with caution.
If you want to dive deeper, let me know:
• What astronomical catalog your data comes from (e.g., Gaia DR3)
• If you also need to convert this into a physical tangential velocity (km/s) using the object's distance or parallax"


