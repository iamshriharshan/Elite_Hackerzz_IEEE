function validateFile() {
    var fileInput = document.getElementById('fileInput');
    var errorMessage = document.getElementById('errorMessage');
    
    // Check if any file is selected
    if (fileInput.files.length === 0) {
        errorMessage.innerHTML = "Please select a file.";
        return false;
    }

    // Access the selected file
    var file = fileInput.files[0];
    
    // Check file type
    var allowedTypes = ["text/txt", "text/pdf", "text/docx"];
    if (!allowedTypes.includes(file.type)) {
        errorMessage.innerHTML = "Please select a valid image file (TXT,PDF,DOCX).";
        return false;
    }}