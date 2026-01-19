from django.db import models
from django.contrib.auth.models import User
from .services import extract_text_from_file
 

class MedicalReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='reports/')
    extracted_text = models.TextField(blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)
    abnormal_findings = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.report_file and not self.extracted_text:
            self.extracted_text = extract_text_from_file(self.report_file.path)
            super().save(update_fields=["extracted_text"])
            self.generate_ai_results()


    def __str__(self):
        return f"Report {self.id} - {self.user.username}"
    
    

    def generate_ai_insights(self):
        from .ai_utils import explain_medical_text
        prompt = f"Explain this medical report text in simple language:\n\n{self.extracted_text}"
        result = explain_medical_text(prompt)
        # You can parse result into summary/suggestions etc.
        self.ai_summary = result
        self.save(update_fields=["ai_summary"])


    def generate_ai_results(self):
        if not self.extracted_text:
            return
        from .ai_services import analyze_report
        ai_output = analyze_report(self.extracted_text)

        # Simple parsing
        parts = ai_output.split("ABNORMAL FINDINGS:")
        summary_part = parts[0].replace("SUMMARY:", "").strip()

        rest = parts[1].split("LIFESTYLE SUGGESTIONS:")
        abnormal_part = rest[0].strip()
        suggestion_part = rest[1].strip()

        self.ai_summary = summary_part
        self.abnormal_findings = abnormal_part
        self.suggestions = suggestion_part
        self.save(update_fields=["ai_summary", "abnormal_findings", "suggestions"])

    def filename(self):
        return self.report_file.name.split('/')[-1]





# from .ai_utils import explain_medical_text

# def generate_ai_insights(self):
#     prompt = f"Explain this medical report text in simple language:\n\n{self.extracted_text}"
#     result = explain_medical_text(prompt)
#     # You can parse result into summary/suggestions etc.
#     self.ai_summary = result
#     self.save(update_fields=["ai_summary"])
