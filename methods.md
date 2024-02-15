I
1. Using Django's Messages Framework: Django provides a built-in messages framework that allows you to display messages to users after a request is processed. To use this framework, you need to add `Django.contrib.messages.middleware.Message-middleware` to your `MIDDLEWARE` settings and add `Django.contrib.messages` to your `INSTALLED_APPS`. Then, you can add messages in your views using the `messages` module. For example:

CODE:

from Django.contrib import messages

def my_view(request):
    # Some processing
    messages.success(request, 'Success message.')
    # or
    messages.error(request, 'Error message.')


In your HTML templates, you can render these messages using something like:


{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}


2.Using Context Variables: You can pass success and error messages as context variables from your views to your templates and then display them directly in your HTML.

CODE:


def my_view(request):
    # Some processing
    success_message = "Success message."
    error_message = "Error message."
    return render(request, 'my_template.html', {'success_message': success_message, 'error_message': error_message})


And in your HTML template:


{% if success_message %}
    <p class="success">{{ success_message }}</p>
{% endif %}
{% if error_message %}
    <p class="error">{{ error_message }}</p>
{% endif %}











3.Using AJAX : You can use JavaScript to handle form submissions asynchronously and display success or error messages dynamically without reloading the entire page.



<!DOCTYPE html>
<html>
<head>
    <title>Feedback Form</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            $('#feedback-form').on('submit', function(event){
                event.preventDefault(); // Prevent default form submission

                // Serialize form data
                var formData = $(this).serialize();

                // AJAX POST request
                $.ajax({
                    type: 'POST',
                    url: '{% url "submit_feedback" %}',
                    data: formData,
                    success: function(response){
                        $('#feedback-message').text(response.message).removeClass('error').addClass('success');
                    },
                    error: function(xhr, status, error){
                        $('#feedback-message').text(xhr.responseJSON.message).removeClass('success').addClass('error');
                    }
                });
            });
        });
    </script>
</head>
<body>
    <h1>Feedback Form</h1>
    <form id="feedback-form" method="post">
        {% csrf_token %}
        <label for="feedback">Feedback:</label><br>
        <textarea id="feedback" name="feedback" rows="4" cols="50"></textarea><br>
        <button type="submit">Submit Feedback</button>
    </form>
    <div id="feedback-message"></div>
</body>
</html>


