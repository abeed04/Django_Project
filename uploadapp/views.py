import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.shortcuts import redirect

def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if file and file.name.endswith(('.csv', '.xlsx')):
            # Save file temporarily to read it
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            filepath = fs.path(filename)

            # Load the data with pandas
            if file.name.endswith('.csv'):
                data = pd.read_csv(filepath)
            else:
                data = pd.read_excel(filepath)

            # Process the summary data here (Step 3)
            summary = {
                "row_count": data.shape[0],
                "column_count": data.shape[1],
                "columns": data.columns.tolist(),
            }
            # Pass summary to template for display
            return render(request, "uploadapp/summary.html", {"summary": summary})

    return render(request, "uploadapp/upload.html")

def send_email(request):
    # Retrieve the summary from session
    summary = request.session.get('summary')
    if not summary:
        return redirect('upload_file')  # Redirect if there's no summary data

    # Prepare the email content
    subject = "Python Assignment - Your Name"
    message = (
        f"Summary Report:\n"
        f"Rows: {summary['row_count']}\n"
        f"Columns: {summary['column_count']}\n"
        f"Column Names: {', '.join(summary['columns'])}"
    )
    recipient_list = ["tech@themedius.ai"]

    # Send the email
    send_mail(
        subject,
        message,
        'mohammedabeed1804@gmail.com',
        recipient_list,
    )
    return redirect("upload_file") 