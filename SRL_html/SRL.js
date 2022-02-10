var xel_examples = {
    "eng": [
		"To achieve her mission, she opened schools to teach young women her philosophy of dance.",
        "Duncan disliked the commercial aspects of public performance, such as touring and contracts, because she felt they distracted her from her real mission, namely the creation of beauty and the education of the young.",
        "A meteor procession was visible across much of eastern North and South America, leading astronomers to conclude that its source was a small, short-lived natural satellite of the Earth.",
        "Semantic parsing of sentences is believed to be an important task on the road to natural language understanding, and has immediate applications in tasks such as information extraction and question answering.",
        "His duties will be assumed by John Smith who has been elected deputy chairman.",
        "The eruption of an underwater volcano near Tonga on Saturday was likely the biggest recorded anywhere on the planet in more than 30 years, according to experts. Dramatic images from space captured the eruption in real time, as a huge plume of ash, gas and steam was spewed up to 20 kilometers into the atmosphere and tsunami waves were sent crashing across the Pacific.",
        "Crews fighting a massive fire along the central coast of California near the iconic Highway 1 made progress Sunday in containing the blaze, but dozens of homes remained under evacuation orders. The Colorado fire ignited Friday evening in Palo Colorado Canyon in the Big Sur region of Monterey County and swelled to 1050 acres Saturday, up from 100 acres a day prior.", 
        "Pfizer and BioNTech have begun a clinical trial for their Omicron-specific Covid-19 vaccine candidate, they announced in a news release on Tuesday. The study will evaluate the vaccine for safety, tolerability and the level of immune response, as both a primary series and a booster dose, in up to 1420 healthy adults ages 18 to 55."

]
}

function fillExampleSelectField() {
	hideResult();
	lang="eng";
	// alert("examples...");
	$("#example").empty();
	selectField = document.getElementById("example");
	textField = document.getElementById("text");
	idx = 0;
	for (var example in xel_examples[lang]) {
		var opt = document.createElement("option");
		opt.value=idx;
		opt.innerHTML = xel_examples[lang][idx].substring(0,50)+"..."; 
		selectField.appendChild(opt);
		idx += 1;
	}	
	selectField.value = "0";
	textField.value = xel_examples[lang][0];
}

function newExampleSelect() {
	hideResult();
	// langSelectField = document.getElementById("lang");
	lang = "eng"; // langSelectField.value;
	exampleSelectField = document.getElementById("example");
	example = exampleSelectField.value;
	textField = document.getElementById("text");
	// textField.value = xel_langs[languageSelected]["text"]; 
	textField.value = xel_examples[lang][example]; 
}

function getSelectedAnnotators() {
	var selectedAnnotators = [];
	var annotator_buttons = document.getElementsByClassName('annotator');
	for(var i = 0; i<annotator_buttons.length;i++)
	{
		var ann_button = annotator_buttons[i];
		//console.log(checkbox_button);
		if(ann_button.checked) {
			//alert(ann_button.id);
			var text_of_button = ann_button.id;
			//console.log(text_of_button);
			selectedAnnotators.push(text_of_button);
		}
	}
	return selectedAnnotators;
}

function hideResult() {
	$("#result").hide();
	$("#result").html("");
}

function showResult() {
	$("#result").show();
}

/*
async function httpPOST(url = '', data = {}, pfunction) {
  console.log(url);
  console.log(JSON.stringify(data));
  fetch(url, {
    method: 'POST',
    mode: 'no-cors',
	cache: 'no-cache',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(resp => resp.json())
        .then(json => {
                pfunction(json);
        });
}
*/

async function postInput(url = '', data = {}) {
	const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //mode: 'no-cors', // no-cors, *cors, same-origin
    // cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    // credentials: 'omit', // include, *same-origin, omit
    headers: {
        'Content-Type': 'application/json',
       // 'Accept': 'application/json, text/plaini, */*'
      //'Content-Type': 'application/json'
        //,'Data-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    // redirect: 'follow', // manual, *follow, error
    // referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
    //body: data
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

function formSubmit() {
	hideResult();
	$("#result").html("Working...");
	showResult();
	anns = getSelectedAnnotators();
	text = document.getElementById("text").value;
	data = {
		"text": text,
		"anns": anns
	};
	url = "view";
	postInput(url, data)
		.then(data => {
			// console.log(data);
			$("#result").html(data.html);
			showResult();
    });
	// $("#result").html(anns.join(","));
	// showResult();
	return false;
}

function showSenseFrameVerb(predicate,senseNumber)
{
	$("#senseFrame").show();
	// $("#senseFrameBody").html("<h1>"+predicate+":"+senseNumber+"</h1>");

	data = {
		"predicate": predicate,
		"senseNumber": senseNumber
	};
	url = "verbSenseFrame";
	postInput(url, data)
		.then(data => {
			// console.log(data);
			$("#senseFrameBody").html(data.html);
			// showResult();
    });

	return false;
}

function showSenseFrameNom(predicate,senseNumber)
{
	$("#senseFrame").show();
	// $("#senseFrameBody").html("<h1>"+predicate+":"+senseNumber+"</h1>");

	data = {
		"predicate": predicate,
		"senseNumber": senseNumber
	};
	url = "nomSenseFrame";
	postInput(url, data)
		.then(data => {
			// console.log(data);
			$("#senseFrameBody").html(data.html);
			// showResult();
    });

	return false;
}

function hideSenseFrame()
{
	// document.getElementById('id01').style.display='none';
	$("#senseFrame").hide();
	$("#senseFrameBody").html("<p>Loading frame content...</p>");
	return false;
}

function main() {
	fillExampleSelectField();
}


