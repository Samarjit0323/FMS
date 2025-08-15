// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
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

	// Menu toggle functionality (for mobile)
	const menuToggle = document.querySelector('.menu-toggle');
	const sidebar = document.querySelector('.sidebar');
	
	if (menuToggle && sidebar) {
		menuToggle.addEventListener('click', () => {
			sidebar.classList.toggle('collapsed');
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

// Chart functionality
function initializeChart() {
	const chartContainer = document.getElementById('analyticsChart');
	if (chartContainer) {
		// Create a simple chart placeholder
		const ctx = chartContainer.getContext('2d');
		ctx.fillStyle = '#667eea';
		ctx.font = '16px Arial';
		ctx.textAlign = 'center';
		ctx.fillText('Chart will be displayed here', 200, 100);
		ctx.fillText('Select period to view analytics', 200, 130);
	}
}

function updateChart(period) {
	const chartContainer = document.getElementById('analyticsChart');
	if (chartContainer) {
		const ctx = chartContainer.getContext('2d');
		ctx.clearRect(0, 0, 400, 200);
		
		// Simple chart visualization
		ctx.fillStyle = '#667eea';
		ctx.font = '14px Arial';
		ctx.textAlign = 'center';
		ctx.fillText(`Analytics for last ${period} days`, 200, 100);
		
		// Draw a simple bar chart
		const data = generateSampleData(period);
		drawBarChart(ctx, data);
	}
}

function generateSampleData(period) {
	const data = [];
	for (let i = 0; i < period; i++) {
		data.push(Math.floor(Math.random() * 100) + 20);
	}
	return data;
}

function drawBarChart(ctx, data) {
	const barWidth = 300 / data.length;
	const maxValue = Math.max(...data);
	const chartHeight = 120;
	const startX = 50;
	const startY = 180;
	
	ctx.fillStyle = '#667eea';
	data.forEach((value, index) => {
		const barHeight = (value / maxValue) * chartHeight;
		const x = startX + (index * barWidth);
		const y = startY - barHeight;
		
		ctx.fillRect(x, y, barWidth - 2, barHeight);
	});
}

// Quick action handler
function handleQuickAction(action) {
	switch(action) {
		case 'Add User':
			alert('Add User functionality will be implemented here');
			break;
		case 'Generate Report':
			alert('Report generation will be implemented here');
			break;
		case 'System Settings':
			alert('System settings will be implemented here');
			break;
		case 'Get Help':
			alert('Help system will be implemented here');
			break;
		default:
			console.log('Action:', action);
	}
}

// Personal Section Modal Functions
function openPersonalSection() {
	document.getElementById('personalSectionModal').style.display = 'block';
	document.body.style.overflow = 'hidden';
}

function closePersonalSection() {
	document.getElementById('personalSectionModal').style.display = 'none';
	document.body.style.overflow = 'auto';
}

// Tab switching functionality
function showTab(tabName) {
	// Hide all tab contents
	const tabContents = document.querySelectorAll('.tab-content');
	tabContents.forEach(content => {
		content.classList.remove('active');
	});
	
	// Remove active class from all tab buttons
	const tabButtons = document.querySelectorAll('.tab-btn');
	tabButtons.forEach(btn => {
		btn.classList.remove('active');
	});
	
	// Show selected tab content
	document.getElementById(tabName).classList.add('active');
	
	// Add active class to clicked button
	event.target.classList.add('active');
}

// CSV Operations
function importCSV() {
	const input = document.createElement('input');
	input.type = 'file';
	input.accept = '.csv';
	input.onchange = function(e) {
		const file = e.target.files[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = function(e) {
				parseCSV(e.target.result);
			};
			reader.readAsText(file);
		}
	};
	input.click();
}

function exportCSV() {
	const table = document.getElementById('csvTableBody');
	let csv = 'Name,Email,Phone,Department\n';
	
	const rows = table.querySelectorAll('tr');
	rows.forEach(row => {
		const cells = row.querySelectorAll('td');
		const rowData = [];
		cells.forEach((cell, index) => {
			if (index < 4) { // Exclude Actions column
				rowData.push(cell.textContent);
			}
		});
		csv += rowData.join(',') + '\n';
	});
	
	downloadCSV(csv, 'personal_data.csv');
}

function downloadTemplate() {
	const template = 'Name,Email,Phone,Department\nJohn Doe,john@example.com,+1234567890,Computer Science\nJane Smith,jane@example.com,+1234567891,Mathematics';
	downloadCSV(template, 'personal_data_template.csv');
}

function parseCSV(csvText) {
	const lines = csvText.split('\n');
	const tableBody = document.getElementById('csvTableBody');
	tableBody.innerHTML = '';
	
	lines.forEach((line, index) => {
		if (index === 0 || line.trim() === '') return; // Skip header and empty lines
		
		const cells = line.split(',');
		if (cells.length >= 4) {
			const row = document.createElement('tr');
			row.innerHTML = `
				<td>${cells[0] || ''}</td>
				<td>${cells[1] || ''}</td>
				<td>${cells[2] || ''}</td>
				<td>${cells[3] || ''}</td>
				<td>
					<button class="btn-small btn-edit" onclick="editRow(this)">Edit</button>
					<button class="btn-small btn-delete" onclick="deleteRow(this)">Delete</button>
				</td>
			`;
			tableBody.appendChild(row);
		}
	});
}

function downloadCSV(csvContent, filename) {
	const blob = new Blob([csvContent], { type: 'text/csv' });
	const url = window.URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = filename;
	a.click();
	window.URL.revokeObjectURL(url);
}

// Table row operations
function editRow(button) {
	const row = button.closest('tr');
	const cells = row.querySelectorAll('td');
	
	cells.forEach((cell, index) => {
		if (index < 4) { // Exclude Actions column
			const currentText = cell.textContent;
			const input = document.createElement('input');
			input.type = 'text';
			input.value = currentText;
			input.className = 'edit-input';
			cell.textContent = '';
			cell.appendChild(input);
			input.focus();
			
			input.addEventListener('blur', function() {
				cell.textContent = this.value;
			});
			
			input.addEventListener('keypress', function(e) {
				if (e.key === 'Enter') {
					cell.textContent = this.value;
				}
			});
		}
	});
}

function deleteRow(button) {
	if (confirm('Are you sure you want to delete this row?')) {
		button.closest('tr').remove();
	}
}

// File Upload Functions
function handleFileUpload(event) {
	const files = event.target.files;
	
	files.forEach(file => {
		if (isValidFileType(file)) {
			displayUploadedFile(file);
		} else {
			alert(`Invalid file type: ${file.name}. Please upload only PDF, JPG, JPEG, or PNG files.`);
		}
	});
}

function isValidFileType(file) {
	const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
	return validTypes.includes(file.type);
}

function displayUploadedFile(file) {
	const uploadedFiles = document.getElementById('uploadedFiles');
	const fileItem = document.createElement('div');
	fileItem.className = 'file-item';
	
	const fileIcon = getFileIcon(file.type);
	const fileSize = formatFileSize(file.size);
	
	fileItem.innerHTML = `
		<div class="file-info">
			<div class="file-icon">
				${fileIcon}
			</div>
			<div class="file-details">
				<h4>${file.name}</h4>
				<p>${fileSize} • ${file.type}</p>
			</div>
		</div>
		<div class="file-actions">
			<button onclick="downloadFile('${file.name}')" style="background: #28a745; color: white;">Download</button>
			<button onclick="deleteFile(this)" style="background: #dc3545; color: white;">Delete</button>
		</div>
	`;
	
	uploadedFiles.appendChild(fileItem);
}

function getFileIcon(fileType) {
	switch(fileType) {
		case 'application/pdf':
			return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/></svg>';
		case 'image/jpeg':
		case 'image/jpg':
		case 'image/png':
			return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/><path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-12zm12 1a1 1 0 0 1 1 1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 1-1h12z"/></svg>';
		default:
			return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/></svg>';
	}
}

function formatFileSize(bytes) {
	if (bytes === 0) return '0 Bytes';
	const k = 1024;
	const sizes = ['Bytes', 'KB', 'MB', 'GB'];
	const i = Math.floor(Math.log(bytes) / Math.log(k));
	return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function downloadFile(filename) {
	alert(`Download functionality for ${filename} will be implemented here`);
}

function deleteFile(button) {
	if (confirm('Are you sure you want to delete this file?')) {
		button.closest('.file-item').remove();
	}
}

// Close modal when clicking outside
window.onclick = function(event) {
	const modal = document.getElementById('personalSectionModal');
	if (event.target === modal) {
		closePersonalSection();
	}
}
