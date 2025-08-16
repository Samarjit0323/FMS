// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
	// Load and display user information
	loadUserInfo();
	
	// Check if user is logged in
	checkAuth();
	
	// Dark/Light Mode Toggle
	const darkLightToggle = document.querySelector('.dark-light-toggle');
	if (darkLightToggle) {
		darkLightToggle.addEventListener('click', () => {
			document.body.classList.toggle('system-default');
		});
	}

	// Profile Dropdown Toggle
	const profileDropdown = document.querySelector('.profile-dropdown');
	const dropdownMenu = document.querySelector('.dropdown-menu');

	if (profileDropdown && dropdownMenu) {
		profileDropdown.addEventListener('click', () => {
			dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
		});

		// Close dropdown if clicked outside
		document.addEventListener('click', (e) => {
			if (!profileDropdown.contains(e.target)) {
				dropdownMenu.style.display = 'none';
			}
		});
	}

	// Sidebar toggle functionality
	const menuToggle = document.querySelector('.menu-toggle');
	const sidebar = document.querySelector('.sidebar');
	const mainContent = document.querySelector('.main-content');
	
	if (menuToggle && sidebar) {
		menuToggle.addEventListener('click', () => {
			console.log('Menu toggle clicked');
			
			// Toggle the open state (slide in/out)
			sidebar.classList.toggle('open');
			mainContent.classList.toggle('shift');
			
			// If sidebar is open, remove collapsed state
			if (sidebar.classList.contains('open')) {
				sidebar.classList.remove('collapsed');
			}
			
			console.log('Sidebar classes:', sidebar.classList.toString());
		});
	}

	// Auto close sidebar if clicking outside
	document.addEventListener('click', (e) => {
		if (sidebar.classList.contains('open') &&
			!sidebar.contains(e.target) &&
			!menuToggle.contains(e.target)) {
			sidebar.classList.remove('open');
			mainContent.classList.remove('shift');
		}
	});

	// Double-click to toggle collapse state (width only)
	if (sidebar) {
		sidebar.addEventListener('dblclick', () => {
			console.log('Sidebar double-clicked');
			
			// Only toggle collapse if sidebar is open
			if (sidebar.classList.contains('open')) {
				sidebar.classList.toggle('collapsed');
				console.log('Sidebar classes after double-click:', sidebar.classList.toString());
			}
		});
	}

	// Chart period selector
	const chartPeriod = document.getElementById('chartPeriod');
	if (chartPeriod) {
		chartPeriod.addEventListener('change', function() {
			updateChart(this.value);
		});
	}

	// Quick action buttons
	const actionButtons = document.querySelectorAll('.action-btn');
	actionButtons.forEach(button => {
		button.addEventListener('click', function() {
			const action = this.querySelector('span').textContent;
			handleQuickAction(action);
		});
	});

	// Initialize chart
	initializeChart();
});

// --- Rest of your existing functions remain unchanged ---
// loadUserInfo(), checkAuth(), logout(), chart functions, modals, etc.

// Add missing functions
function loadUserInfo() {
	// Placeholder for user info loading
	console.log('Loading user info...');
}

function checkAuth() {
	// Placeholder for authentication check
	console.log('Checking authentication...');
}

function logout() {
	// Placeholder for logout functionality
	console.log('Logging out...');
	// Redirect to login page or show logout message
}

function updateChart(period) {
	// Placeholder for chart update
	console.log('Updating chart for period:', period);
}

function handleQuickAction(action) {
	// Placeholder for quick action handling
	console.log('Handling quick action:', action);
}

function initializeChart() {
	// Placeholder for chart initialization
	console.log('Initializing chart...');
}

// Modal functions
function openPersonalSection() {
	document.getElementById('personalSectionModal').style.display = 'block';
}

function closePersonalSection() {
	document.getElementById('personalSectionModal').style.display = 'none';
}

function openAcademicsSection() {
	document.getElementById('academicsSectionModal').style.display = 'block';
}

function closeAcademicsSection() {
	document.getElementById('academicsSectionModal').style.display = 'none';
}

function openServiceSection() {
	document.getElementById('serviceSectionModal').style.display = 'block';
}

function closeServiceSection() {
	document.getElementById('serviceSectionModal').style.display = 'none';
}

function openFacultyStatsSection() {
	document.getElementById('facultyStatsModal').style.display = 'block';
}

function closeFacultyStatsSection() {
	document.getElementById('facultyStatsModal').style.display = 'none';
}

// Tab functions
function showTab(tabName) {
	// Hide all tab contents
	const tabContents = document.querySelectorAll('.tab-content');
	tabContents.forEach(content => content.classList.remove('active'));
	
	// Remove active class from all tab buttons
	const tabButtons = document.querySelectorAll('.tab-btn');
	tabButtons.forEach(button => button.classList.remove('active'));
	
	// Show selected tab content
	document.getElementById(tabName).classList.add('active');
	
	// Add active class to clicked button
	event.target.classList.add('active');
}

function showAcademicsTab(tabName) {
	// Hide all tab contents
	const tabContents = document.querySelectorAll('.tab-content');
	tabContents.forEach(content => content.classList.remove('active'));
	
	// Remove active class from all tab buttons
	const tabButtons = document.querySelectorAll('.academics-tabs .tab-btn');
	tabButtons.forEach(button => button.classList.remove('active'));
	
	// Show selected tab content
	document.getElementById(tabName).classList.add('active');
	
	// Add active class to clicked button
	event.target.classList.add('active');
}

function showServiceTab(tabName) {
	// Hide all tab contents
	const tabContents = document.querySelectorAll('.tab-content');
	tabContents.forEach(content => content.classList.remove('active'));
	
	// Remove active class from all tab buttons
	const tabButtons = document.querySelectorAll('.service-tabs .tab-btn');
	tabButtons.forEach(button => button.classList.remove('active'));
	
	// Show selected tab content
	document.getElementById(tabName).classList.add('active');
	
	// Add active class to clicked button
	event.target.classList.add('active');
}

function showStatsTab(tabName) {
	// Hide all tab contents
	const tabContents = document.querySelectorAll('.tab-content');
	tabContents.forEach(content => content.classList.remove('active'));
	
	// Remove active class from all tab buttons
	const tabButtons = document.querySelectorAll('.stats-tabs .tab-btn');
	tabButtons.forEach(button => button.classList.remove('active'));
	
	// Add active class to clicked button
	event.target.classList.add('active');
	
	// Show selected tab content
	document.getElementById(tabName).classList.add('active');
}

// CSV and data functions
function importCSV() {
	console.log('Import CSV clicked');
}

function exportCSV() {
	console.log('Export CSV clicked');
}

function downloadTemplate() {
	console.log('Download template clicked');
}

function handleFileUpload(event) {
	console.log('File upload:', event.target.files);
}

// Other action functions
function addCourse() { console.log('Add course clicked'); }
function exportCourses() { console.log('Export courses clicked'); }
function importCourses() { console.log('Import courses clicked'); }
function addAssignment() { console.log('Add assignment clicked'); }
function exportAssignments() { console.log('Export assignments clicked'); }
function addGrade() { console.log('Add grade clicked'); }
function exportGrades() { console.log('Export grades clicked'); }
function addProject() { console.log('Add project clicked'); }
function exportProjects() { console.log('Export projects clicked'); }
function addConsultation() { console.log('Add consultation clicked'); }
function exportConsultations() { console.log('Export consultations clicked'); }
function addPublication() { console.log('Add publication clicked'); }
function exportPublications() { console.log('Export publications clicked'); }
function generateReport() { console.log('Generate report clicked'); }
function exportReport() { console.log('Export report clicked'); }
function scheduleReport() { console.log('Schedule report clicked'); }
function updatePerformanceChart(period) { console.log('Update performance chart:', period); }