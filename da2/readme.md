# Prototype Data Analysis - V2

Note: This is just an alternative to the V1 UI in [da](https://github.com/DeniseMak/nlpstats-proto/tree/master/da) 
to try out a submit button. We can decide tomorrow (7/22) which kind of submit button works better after
this version has been fleshed out.
 
## State of Affairs
* We have working text input and output.
* File upload now saves the chosen file into the [da2](https://github.com/DeniseMak/nlpstats-proto/tree/master/da2) directory
* We have working creation of SVG and display based on data, using Haotian's function.
* Radio buttons not working

## Todo (Data Analysis Tab -- We Have More!)
0. **Should not crash on submission without file**
1. Refocus form on the correct tab after submission. 
2. Finish plumbing the other functions written by Haotian.
3. Client-side validation. 
4. Passing of server-side validation errors.
5. Aesthetic improvements.
6. Code cleanup and commenting.

## Changes
* How to hide the file input label [SA answer](https://stackoverflow.com/questions/16001586/change-the-no-file-chosen). We can use the `{ {xyz} }` syntax to say that a file is already picked if that is the case. I also used this: [SA text as button](https://stackoverflow.com/questions/710089/how-do-i-make-an-html-link-look-like-a-button)
* Help function plumbing. [tooltips](https://www.w3schools.com/howto/howto_css_tooltip.asp)
* Default data form values.  Change `placeholder` to `value`.
* Retain values on submission.


## Resources

* Note: unlike the example in the [da](https://github.com/DeniseMak/nlpstats-proto/tree/master/da) directory, the route function calls
 `render_template()` instead of `jsonify`.

This subdirectory has my work on the project so far. A lot of it is plumbed together from the following links.

* https://stackoverflow.com/questions/46698134/how-to-post-the-output-result-on-the-same-page-in-flask-app
* https://stackoverflow.com/questions/46785507/python-flask-display-image-on-a-html-page
* https://stackoverflow.com/questions/5451445/how-to-display-image-with-javascript#5454306
* https://stackoverflow.com/questions/10859930/how-to-display-a-div-triggered-by-onclick-event
* https://stackoverflow.com/questions/6019845/show-hide-div-on-click-with-css
* https://bootsnipp.com/forms
* https://www.w3schools.com/howto/howto_js_tabs.asp
