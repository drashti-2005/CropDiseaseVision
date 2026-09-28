// ====== TRANSLATION CONFIGURATION ======
const LANGUAGE_MAP = {
	English: "en",
	Hindi: "hi",
	Gujarati: "gu",
	Marathi: "mr",
	Tamil: "ta",
	Telugu: "te",
};

const VOICE_LANG_MAP = {
	English: "en-US",
	Hindi: "hi-IN",
	Gujarati: "gu-IN",
	Marathi: "mr-IN",
	Tamil: "ta-IN",
	Telugu: "te-IN",
};

let currentLanguage = "English";
let translationCache = {};

// ====== SIMPLE TRANSLATION FUNCTION ======
async function translateText(text, lang) {
	console.log(`\n📝 translateText() called: text="${text}", lang="${lang}"`);

	// No translation needed for English
	if (lang === "English" || !text) {
		console.log("   ➜ English or empty text, returning as-is");
		return text;
	}

	// Check cache
	const key = `${text}||${lang}`;
	if (translationCache[key]) {
		console.log(`   ✅ CACHED: "${translationCache[key]}"`);
		return translationCache[key];
	}

	try {
		const code = LANGUAGE_MAP[lang];
		console.log(`   🔄 Language code: "${lang}" → "${code}"`);

		if (!code) {
			console.log("   ⚠️ Invalid language code, returning original");
			return text;
		}

		console.log(`   🌐 Calling Backend Translation API...`);

		// Call backend translation endpoint (avoids CORS issues)
		const response = await fetch("http://127.0.0.1:5000/api/translate", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				text: text,
				target_language: code,
			}),
		});

		if (!response.ok) {
			throw new Error(`Backend API returned ${response.status}`);
		}

		const data = await response.json();
		const result = data.translated_text || text;

		translationCache[key] = result;
		console.log(`   ✅ API Response: "${result}"`);

		return result;
	} catch (error) {
		console.error(`   ❌ Translation error: ${error.message}`);
		console.log(`   ➜ Returning original text: "${text}"`);
		return text;
	}
}

// ====== TRANSLATE TO ENGLISH ======
// ====== SHOW TRANSLATION LOADING ======
function showTranslationLoading(show = true) {
	let statusDiv = document.getElementById("translationStatus");

	if (!statusDiv) {
		statusDiv = document.createElement("div");
		statusDiv.id = "translationStatus";
		statusDiv.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 999;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 12px rgba(243, 156, 18, 0.3);
        `;
		document.body.appendChild(statusDiv);
	}

	if (show) {
		statusDiv.innerHTML =
			'<i class="fas fa-spinner fa-spin"></i> Translating...';
		statusDiv.style.display = "flex";
	} else {
		statusDiv.style.display = "none";
	}
}

// DOM Elements
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const predictBtn = document.getElementById("predictBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const diseaseNameSpan = document.getElementById("diseaseName");
const confidenceLevelSpan = document.getElementById("confidenceLevel");
const confidenceBar = document.getElementById("confidenceBar");
const errorDiv = document.getElementById("error");
const errorMessage = document.getElementById("errorMessage");
const resetBtn = document.getElementById("resetBtn");
const actionsList = document.getElementById("actionsList");
const historyList = document.getElementById("historyList");
const languageSelector = document.getElementById("languageSelector");

// ====== TAB SWITCHING LOGIC ======
function switchTab(tabName) {
	document.getElementById("tabImage").classList.remove("active");
	document.getElementById("contentImage").classList.remove("active");
	document.getElementById("contentImage").style.display = "none";
	document.getElementById("tabImage").classList.add("active");
	document.getElementById("contentImage").classList.add("active");
	document.getElementById("contentImage").style.display = "block";
}

let analysisHistory = [];

// ====== LANGUAGE SELECTOR INTEGRATION ======
if (languageSelector) {
	console.log("\n🌍 Initializing Language Selector...");

	// Load saved language preference
	const savedLanguage = localStorage.getItem("selectedLanguage");
	console.log("   📦 Saved language in localStorage:", savedLanguage);

	if (savedLanguage && LANGUAGE_MAP[savedLanguage]) {
		currentLanguage = savedLanguage;
		languageSelector.value = currentLanguage;
		console.log(`   ✅ Set language from localStorage: "${currentLanguage}"`);
	} else {
		console.log(`   ℹ️ No saved language, using default: "${currentLanguage}"`);
	}

	console.log(
		"   📋 Available languages:",
		Object.keys(LANGUAGE_MAP).join(", "),
	);
	console.log("   ✅ Language Selector initialized\n");

	languageSelector.addEventListener("change", (e) => {
		const oldLang = currentLanguage;
		currentLanguage = e.target.value;
		localStorage.setItem("selectedLanguage", currentLanguage);

		console.log(`\n🔄 Language Changed: "${oldLang}" → "${currentLanguage}"`);

		// Retranslate current results if visible
		if (!result.classList.contains("hidden")) {
			console.log("   🔄 Re-translating current results...");
			retranslateCurrentResults();
		}
	});
}

// Image Upload with Drag & Drop
imageInput.addEventListener("change", handleImageUpload);

document.querySelector(".upload-section").addEventListener("dragover", (e) => {
	e.preventDefault();
	document.querySelector(".upload-section").style.borderColor = "#f39c12";
});

document.querySelector(".upload-section").addEventListener("dragleave", (e) => {
	document.querySelector(".upload-section").style.borderColor = "#27ae60";
});

document.querySelector(".upload-section").addEventListener("drop", (e) => {
	e.preventDefault();
	imageInput.files = e.dataTransfer.files;
	handleImageUpload();
});

function isValidImageFile(file) {
	if (!file) return false;

	const fileName = (file.name || "").toLowerCase();
	const validExtensions = /\.(jpe?g|png|gif|bmp|webp|heic|heif|tif|tiff)$/i;
	const mimeIsImage =
		typeof file.type === "string" && file.type.startsWith("image/");

	return mimeIsImage || validExtensions.test(fileName);
}

function handleImageUpload() {
	const file = imageInput.files[0];

	clearResults();

	if (isValidImageFile(file)) {
		const reader = new FileReader();
		reader.onload = (e) => {
			imagePreview.src = e.target.result;
			imagePreview.style.display = "block";
			predictBtn.disabled = false;
		};
		reader.readAsDataURL(file);
	} else {
		showError("Please select a valid image file (JPG, PNG, etc.)");
		imagePreview.style.display = "none";
		predictBtn.disabled = true;
	}
}

// Image prediction
predictBtn.addEventListener("click", predictImage);

async function predictImage() {
	const file = imageInput.files[0];

	if (!file) {
		showError("Please select an image first (Required)");
		return;
	}

	const formData = new FormData();
	formData.append("file", file);
	showLoading(true);

	try {
		const response = await fetch("http://127.0.0.1:5000/api/predict", {
			method: "POST",
			body: formData,
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();
		displayResults(data, "image");
	} catch (error) {
		console.error("Error:", error);
		showError(
			`Failed to connect to backend. Make sure the server is running on http://127.0.0.1:5000`,
		);
	} finally {
		showLoading(false);
	}
}

async function displayResults(data, source = "image") {
	console.log("════════════════════════════════════════");
	console.log("🔍 DISPLAYING RESULTS");
	console.log("════════════════════════════════════════");
	clearResults();
	showTranslationLoading(true);

	try {
		const diseaseName = data.disease || "Unknown";
		const confidence = (data.confidence * 100).toFixed(2);
		const formattedName = diseaseName.replace(/___/g, " - ").replace(/_/g, " ");

		console.log("📍 Selected Language:", currentLanguage);
		console.log("📍 Disease (from backend):", diseaseName);
		console.log("📍 Disease (formatted):", formattedName);
		console.log("📍 Confidence:", confidence + "%");

		// TRANSLATE the disease name if not English
		let displayName = formattedName;
		if (currentLanguage !== "English") {
			console.log("🌍 Translating disease name to", currentLanguage);
			displayName = await translateText(formattedName, currentLanguage);
			console.log("✅ Disease name translated:", displayName);
		} else {
			console.log("🔤 Language is English, no translation needed");
		}

		// Update UI with translated name
		diseaseNameSpan.textContent = displayName;
		confidenceLevelSpan.textContent = `${confidence}%`;
		confidenceBar.style.width = `${confidence}%`;
		console.log("✅ Disease name updated in UI:", displayName);

		// Get and translate recommendations
		console.log("🌍 Getting recommendations for:", diseaseName);
		const recs = await getTranslatedRecommendations(diseaseName);
		console.log("✅ Recommendations received:", recs.length, "items");
		recs.forEach((rec, i) => console.log(`  [${i + 1}] ${rec}`));

		actionsList.innerHTML = recs.map((r) => `<li>${r}</li>`).join("");

		// Add to history
		addToHistory(diseaseName, confidence, source);

		// Setup audio
		setupSpeechButton(displayName, confidence);

		result.classList.remove("hidden");
		console.log("════════════════════════════════════════");
		console.log("✨ RESULTS DISPLAYED SUCCESSFULLY");
		console.log("════════════════════════════════════════");
	} catch (error) {
		console.error("❌ Error displaying results:", error);
		showError("Error processing results");
	} finally {
		showTranslationLoading(false);
	}
}

// NEW: Get translated recommendations
async function getTranslatedRecommendations(disease) {
	console.log(`\n💡 getTranslatedRecommendations() called for: "${disease}"`);

	const recs = getRecommendations(disease);
	console.log(`   📋 Found ${recs.length} recommendations`);

	if (currentLanguage === "English") {
		console.log("   🔤 Language is English, returning as-is");
		return recs;
	}

	console.log(
		`   🌍 Translating ${recs.length} recommendations to ${currentLanguage}...`,
	);
	try {
		const translated = await Promise.all(
			recs.map((r, i) => {
				console.log(`   [${i + 1}/${recs.length}] Translating: "${r}"`);
				return translateText(r, currentLanguage);
			}),
		);
		console.log(`   ✅ All recommendations translated successfully`);
		return translated;
	} catch (error) {
		console.error(`   ❌ Error translating recommendations:`, error);
		return recs; // Fallback to English if translation fails
	}
}

// ====== SETUP SPEECH FOR RESULT ======
function setupSpeechButton(diseaseName, confidence) {
	const playBtn = document.getElementById("playResultBtn");
	if (!playBtn) return;

	playBtn.onclick = async () => {
		try {
			showTranslationLoading(true);

			// Get current recommendations
			const recs = Array.from(actionsList.querySelectorAll("li"))
				.map((li) => li.textContent)
				.slice(0, 2) // First 2 recommendations
				.join(". ");

			// Build speech text
			let speechText = `Disease detected: ${diseaseName}. Confidence: ${confidence}. Recommended actions: ${recs}`;

			// Create and speak utterance
			const voiceLang = VOICE_LANG_MAP[currentLanguage] || "en-US";
			const utterance = new SpeechSynthesisUtterance(speechText);
			utterance.lang = voiceLang;
			utterance.rate = 0.9; // Slower for clarity
			utterance.pitch = 1.0;
			utterance.volume = 1.0;

			window.speechSynthesis.cancel();
			window.speechSynthesis.speak(utterance);

			console.log(
				`[Speech] Speaking in ${currentLanguage}: ${speechText.substring(0, 50)}...`,
			);
		} catch (error) {
			console.error("Speech error:", error);
			showError("Unable to play audio. Check browser settings.");
		} finally {
			showTranslationLoading(false);
		}
	};
}

// ====== RETRANSLATE RESULTS ON LANGUAGE CHANGE ======
async function retranslateCurrentResults() {
	if (result.classList.contains("hidden")) return;

	showTranslationLoading(true);

	try {
		const currentDisease = diseaseNameSpan.textContent;
		const currentConfidence = confidenceLevelSpan.textContent;

		// Get original disease name from history or try to find it
		const historyItem = analysisHistory[0];
		if (!historyItem) return;

		const originalDisease = historyItem.disease;
		const formattedName = originalDisease
			.replace(/___/g, " - ")
			.replace(/_/g, " ");

		// Translate to new language
		let newName = formattedName;
		if (currentLanguage !== "English") {
			newName = await translateText(formattedName, currentLanguage);
		}

		// Update disease name
		diseaseNameSpan.textContent = newName;

		// Retranslate recommendations
		const recommendations = await getTranslatedRecommendations(originalDisease);
		actionsList.innerHTML = recommendations
			.map((action) => `<li>${action}</li>`)
			.join("");

		// Update speech button
		setupSpeechButton(newName, currentConfidence);

		console.log(`[Retranslate] Results updated to ${currentLanguage}`);
	} catch (error) {
		console.error("Retranslation error:", error);
	} finally {
		showTranslationLoading(false);
	}
}

function getRecommendations(disease) {
	const recommendations = {
		Apple___Apple_scab: [
			"Apply fungicides containing captan or sulfur",
			"Remove infected leaves and dropped fruit",
			"Improve air circulation through pruning",
			"Water at the base to keep foliage dry",
		],
		Apple___Black_rot: [
			"Remove and destroy infected plant parts (mummies, dead wood)",
			"Apply appropriate fungicides during early development",
			"Ensure good air circulation around trees",
		],
		Apple___Cedar_apple_rust: [
			"Remove nearby cedar trees or galls on them",
			"Apply protective fungicides in spring",
			"Plant rust-resistant apple varieties",
		],
		Apple___healthy: [
			"Maintain current watering schedule",
			"Regularly prune for good air flow",
			"Apply preventive dormant oil in late winter",
		],
		Blueberry___healthy: [
			"Maintain acidic soil pH (4.5 to 5.5)",
			"Provide consistent moisture and good drainage",
			"Apply mulch to protect shallow roots",
		],
		"Cherry_(including_sour)___Powdery_mildew": [
			"Apply sulfur or appropriate fungicides",
			"Improve air circulation by pruning",
			"Avoid overhead watering",
		],
		"Cherry_(including_sour)___healthy": [
			"Maintain regular pruning for air circulation",
			"Ensure proper watering and fertilization",
			"Monitor for pests like aphids and fruit flies",
		],
		"Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": [
			"Use resistant crop varieties",
			"Practice crop rotation",
			"Apply foliar fungicides if severe",
		],
		"Corn_(maize)___Common_rust_": [
			"Apply fungicides early when pustules first appear",
			"Plant rust-resistant corn varieties next season",
			"Ensure proper spacing for air circulation",
		],
		"Corn_(maize)___Northern_Leaf_Blight": [
			"Plant resistant hybrids",
			"Rotate crops away from corn",
			"Apply appropriate fungicides during early stages",
		],
		"Corn_(maize)___healthy": [
			"Continue proper fertilization",
			"Maintain consistent watering",
			"Scout regularly for pests",
		],
		Grape___Black_rot: [
			"Remove and destroy infected plant parts",
			"Apply fungicides properly timed with growth stages",
			"Ensure good canopy management for airflow",
		],
		"Grape___Esca_(Black_Measles)": [
			"Prune out infected wood and destroy it",
			"Protect pruning wounds from infection",
			"Avoid stressing vines",
		],
		"Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
			"Apply copper-based fungicides",
			"Improve air circulation in the canopy",
			"Remove fallen leaves in autumn",
		],
		Grape___healthy: [
			"Maintain proper trellis support",
			"Prune regularly to ensure good sunlight penetration",
			"Monitor for pests and diseases regularly",
		],
		"Orange___Haunglongbing_(Citrus_greening)": [
			"Remove and destroy infected trees immediately",
			"Control the Asian citrus psyllid vector",
			"Use certified disease-free nursery stock",
		],
		Peach___Bacterial_spot: [
			"Apply copper-based bactericides in autumn and spring",
			"Plant resistant peach varieties",
			"Avoid excessive nitrogen fertilization",
		],
		Peach___healthy: [
			"Provide proper pruning for light and air",
			"Maintain balanced fertilization",
			"Monitor for peach tree borers and other pests",
		],
		"Pepper,_bell___Bacterial_spot": [
			"Use copper-based bactericides",
			"Avoid overhead watering",
			"Rotate crops away from peppers and tomatoes",
		],
		"Pepper,_bell___healthy": [
			"Maintain consistent watering to prevent blossom end rot",
			"Provide support for heavy fruiting branches",
			"Use mulch to retain soil moisture",
		],
		Potato___Early_blight: [
			"Remove infected leaves immediately",
			"Apply chlorothalonil or copper-based fungicide",
			"Practice crop rotation (avoid planting potatoes in the same spot)",
		],
		Potato___Late_blight: [
			"Apply metalaxyl or mancozeb fungicides",
			"Improve air circulation by proper spacing",
			"Remove and destroy infected plants immediately",
		],
		Potato___healthy: [
			"Maintain consistent soil moisture",
			"Hill potatoes properly",
			"Monitor for Colorado potato beetles",
		],
		Raspberry___healthy: [
			"Prune out old canes after fruiting",
			"Ensure good drainage to prevent root rot",
			"Maintain a regular watering schedule",
		],
		Soybean___healthy: [
			"Ensure proper plant spacing for air flow",
			"Monitor for aphids and other pests",
			"Maintain good weed control",
		],
		Squash___Powdery_mildew: [
			"Apply fungicides or sulfur-based sprays",
			"Improve air circulation by spacing plants",
			"Avoid wetting the leaves when watering",
		],
		Strawberry___Leaf_scorch: [
			"Remove and destroy infected leaves",
			"Ensure proper spacing between plants",
			"Apply protective fungicides during wet weather",
		],
		Strawberry___healthy: [
			"Renew plants every few years",
			"Keep fruit off the soil using mulch",
			"Ensure regular watering but avoid waterlogging",
		],
		Tomato___Bacterial_spot: [
			"Apply copper-based bactericides",
			"Avoid overhead watering (use drip irrigation)",
			"Remove and destroy heavily infected plants",
			"Rotate crops (don't plant tomatoes or peppers in the same spot for 2-3 years)",
		],
		Tomato___Early_blight: [
			"Remove infected leaves (especially lower ones touching the soil)",
			"Apply mancozeb or copper fungicide",
			"Water at soil level only to prevent splashing",
		],
		Tomato___Late_blight: [
			"Apply appropriate fungicides immediately",
			"Remove and destroy infected plants completely",
			"Ensure good air circulation and avoid overhead watering",
		],
		Tomato___Leaf_Mold: [
			"Improve ventilation and air flow",
			"Reduce greenhouse humidity if applicable",
			"Apply appropriate fungicides at first sign of disease",
		],
		Tomato___Septoria_leaf_spot: [
			"Remove infected leaves at the base of the plant",
			"Apply fungicides like chlorothalonil",
			"Use mulch to prevent soil splashing onto leaves",
		],
		"Tomato___Spider_mites Two-spotted_spider_mite": [
			"Use insecticidal soap or horticultural oil",
			"Introduce predatory mites",
			"Keep plants well-watered, as mites thrive in dry conditions",
		],
		Tomato___Target_Spot: [
			"Apply broad-spectrum fungicides",
			"Improve air circulation by pruning lower leaves",
			"Avoid overhead irrigation",
		],
		Tomato___Tomato_Yellow_Leaf_Curl_Virus: [
			"Control whitefly populations (the disease vector)",
			"Remove and destroy infected plants immediately",
			"Use reflective mulches to deter whiteflies",
		],
		Tomato___Tomato_mosaic_virus: [
			"Remove and destroy infected plants immediately",
			"Disinfect tools and wash hands frequently",
			"Avoid smoking near plants (tobacco mosaic virus can cross-infect)",
		],
		Tomato___healthy: [
			"Continue regular watering at the base",
			"Provide adequate support/staking",
			"Apply balanced fertilizer as needed",
		],
		default: [
			"Consult with local agricultural extension",
			"Monitor plant regularly for any changes",
			"Ensure proper irrigation and drainage",
			"Maintain field hygiene and remove weeds",
		],
	};

	return recommendations[disease] || recommendations["default"];
}

function addToHistory(disease, confidence, source) {
	const timestamp = new Date().toLocaleTimeString();
	const historyItem = {
		disease,
		confidence,
		source,
		timestamp,
	};

	analysisHistory.unshift(historyItem);
	if (analysisHistory.length > 10) analysisHistory.pop();

	updateHistoryUI();
	saveToLocalStorage();
}

function updateHistoryUI() {
	historyList.innerHTML = analysisHistory
		.map(
			(item, index) => `
        <div class="history-item" onclick="replayAnalysis(${index})">
            <div class="disease">${item.disease.replace(/___/g, " - ").replace(/_/g, " ")}</div>
            <div class="confidence">${item.confidence}% | ${item.source}</div>
            <div class="time" style="font-size: 0.8rem; color: #95a5a6; margin-top: 5px;">${item.timestamp}</div>
        </div>
    `,
		)
		.join("");
}

function saveToLocalStorage() {
	localStorage.setItem("analysisHistory", JSON.stringify(analysisHistory));
}

function loadFromLocalStorage() {
	const saved = localStorage.getItem("analysisHistory");
	if (saved) {
		analysisHistory = JSON.parse(saved);
		updateHistoryUI();
	}
}

async function replayAnalysis(index) {
	const item = analysisHistory[index];
	const formattedName = item.disease.replace(/___/g, " - ").replace(/_/g, " ");

	let displayName = formattedName;
	if (currentLanguage !== "English") {
		displayName = await translateText(formattedName, currentLanguage);
	}

	diseaseNameSpan.textContent = displayName;
	confidenceLevelSpan.textContent = `${item.confidence}%`;
	confidenceBar.style.width = `${item.confidence}%`;

	const recs = await getTranslatedRecommendations(item.disease);
	actionsList.innerHTML = recs.map((action) => `<li>${action}</li>`).join("");

	setupSpeechButton(displayName, item.confidence);

	result.classList.remove("hidden");
	window.scrollTo({ top: result.offsetTop, behavior: "smooth" });
}

// UI Helpers
function showLoading(show) {
	if (show) {
		loading.classList.remove("hidden");
		result.classList.add("hidden");
		errorDiv.classList.add("hidden");
	} else {
		loading.classList.add("hidden");
	}
}

function showError(message) {
	errorMessage.textContent = message;
	errorDiv.classList.remove("hidden");
	result.classList.add("hidden");
	loading.classList.add("hidden");
}

function clearResults() {
	result.classList.add("hidden");
	errorDiv.classList.add("hidden");
	loading.classList.add("hidden");
}

// Reset Button
resetBtn.addEventListener("click", () => {
	imageInput.value = "";
	imagePreview.style.display = "none";
	predictBtn.disabled = true;
	clearResults();
});

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
	loadFromLocalStorage();
	console.log("CropDiseaseVision v2.0 Ready!");
});
