# Warning Pseudocode

On the homepage, the user can select *Upload Files* or 
*Prospective Power Analysis Tabs* as starting points.

All buttons to selects tabs start out readonly and greyed out, except for 
the *Upload Files* and *Prospective Power Analysis Tabs*

When the user presses the submit button of any tab:
	The contents of that tab become readonly
	The results show below
	The submit button turns into an edit button
	The next tab changes color and becomes clickable
	The identity of tabs is added to a list of completed tabs.
	
When the edit button is pushed:
	That tab becomes editable, if it is edited nothing happends, 
	but on submit a dialogue will ask the user to confirm this will throw
	off later tabs. They can choose not to submit if this is a problem.

When the report button is pressed:
	If the seqeunce of tabs is consistent with 0 1 2 3 4 5 or 0 1 2 3 5:
	     no warning is presented
	If it is not consistent:
	     then an alert says it is not consistent and a red message on report
	     
	     
	     
	     
	     
	     
	     
	     
	     
	     
<script>

   

   function tttt(item, index) {
      document.getElementById(item);
   }

   let recent_tabs = [];

   let all_tabs = ["", "", ""];
   tabs.forEach(tttt);
   
   
   window.onclose = function(){dialog("This will clear your data.");}

</script>

* Add to changeTab: recent_tabs.push(current_tab);
