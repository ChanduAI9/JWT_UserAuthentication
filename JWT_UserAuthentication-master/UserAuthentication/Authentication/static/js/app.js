// Token expiration handling function
function isTokenExpired(token) {
    if (!token) return true;

    const tokenPayload = JSON.parse(atob(token.split('.')[1]));
    const expiryTime = tokenPayload.exp * 1000;  // Convert expiry to milliseconds

    return Date.now() > expiryTime;  // Check if current time is greater than expiry time
}

// Function to refresh the access token using the refresh token
function refreshAccessToken(refreshToken) {
    return $.ajax({
        url: '/api/token/refresh/',  // Use your endpoint for refreshing the token
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ refresh: refreshToken }),
    });
}

$(document).ready(function() {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    // If the access token is expired, try to refresh it
    if (isTokenExpired(accessToken)) {
        if (refreshToken) {
            refreshAccessToken(refreshToken).done(function(response) {
                localStorage.setItem('accessToken', response.access);  // Update access token
                console.log('Access token refreshed');
            }).fail(function() {
                alert('Session has expired. Please log in again.');
                window.location.href = '/login/';  // Redirect to login if refresh token is invalid
            });
        } else {
            alert('Access token has expired. Please log in again.');
            window.location.href = '/login/';  // Redirect to login if no refresh token is available
        }
    } else {
        console.log('Access token is valid.');
    }
});

// Function to make authenticated API requests using the refreshed token
function makeAuthenticatedRequest() {
    const accessToken = localStorage.getItem('accessToken');

    if (isTokenExpired(accessToken)) {
        alert('Your session has expired. Please log in again.');
        window.location.href = '/login/';
        return;
    }

    $.ajax({
        url: '/api/protected-endpoint/',  // Your API endpoint
        type: 'GET',
       
