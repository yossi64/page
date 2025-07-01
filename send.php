<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$to = "yossi16466@gmail.com";

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: index.html");
    exit;
}

$name = isset($_POST['name']) ? htmlspecialchars(trim($_POST['name'])) : '';
$phone = isset($_POST['phone']) ? htmlspecialchars(trim($_POST['phone'])) : '';
$email = isset($_POST['email']) ? htmlspecialchars(trim($_POST['email'])) : '';
$message = isset($_POST['message']) ? htmlspecialchars(trim($_POST['message'])) : '';

if (empty($name) || empty($phone)) {
    die("Error: Name and phone are required fields.");
}

$subject = "🔥 New Lead from Air Duct Cleaning Website - $name";

$body = "NEW LEAD SUBMISSION\n";
$body .= "========================\n\n";
$body .= "Customer Information:\n";
$body .= "Name: $name\n";
$body .= "Phone: $phone\n";
if (!empty($email)) $body .= "Email: $email\n";
$body .= "\nService Details:\n";
$body .= "Service: Air Duct Cleaning\n";
$body .= "Location: San Antonio, TX\n";
$body .= "Price: $129\n";
if (!empty($message)) {
    $body .= "\nCustomer Message:\n";
    $body .= "$message\n";
}
$body .= "\n========================\n";
$body .= "Submitted: " . date('Y-m-d H:i:s T') . "\n";
$body .= "Source: Landing Page Form\n";
$body .= "========================\n";

$domain = $_SERVER['HTTP_HOST'] ?? 'airductcleaning.com';
$from_email = !empty($email) ? $email : "noreply@$domain";
$reply_to = !empty($email) ? $email : $from_email;

$headers = array();
$headers[] = "From: Air Duct Cleaning Lead <$from_email>";
$headers[] = "Reply-To: $reply_to";
$headers[] = "Return-Path: $from_email";
$headers[] = "MIME-Version: 1.0";
$headers[] = "Content-Type: text/plain; charset=UTF-8";
$headers[] = "Content-Transfer-Encoding: 8bit";
$headers[] = "X-Mailer: PHP/" . phpversion();
$headers[] = "X-Priority: 1";
$headers[] = "X-MSMail-Priority: High";
$headers[] = "Importance: High";

$header_string = implode("\r\n", $headers);

$mail_sent = @mail($to, $subject, $body, $header_string);

if ($mail_sent) {
    error_log("SUCCESS: Email sent to $to for lead: $name ($phone) at " . date('Y-m-d H:i:s'));
    header("Location: thankyou.html");
    exit;
} else {
    $error = error_get_last();
    error_log("FAILED: Email not sent to $to for lead: $name ($phone). Error: " . ($error['message'] ?? 'Unknown error'));
    
    echo "<!DOCTYPE html><html><head><title>Thank You</title></head><body>";
    echo "<h2>Thank You for Your Submission!</h2>";
    echo "<p>We have received your information and will contact you soon at <strong>$phone</strong>.</p>";
    echo "<p>If you need immediate assistance, please call us at <strong>(210) 873-0584</strong>.</p>";
    echo "<p><a href='index.html'>Return to main page</a></p>";
    echo "<script>setTimeout(function(){ window.location.href = 'thankyou.html'; }, 5000);</script>";
    echo "</body></html>";
    exit;
}
?>
