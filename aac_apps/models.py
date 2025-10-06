from django.db import models


# Create your models here.
class Kartu(models.Model):
    kartu_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)
    gambar = models.TextField()

    def __str__(self):
        return self.label

    def to_json(self):
        return {"kartu_id": self.kartu_id, "label": self.label, "gambar": self.gambar}

    @classmethod
    def from_json(cls, data):
        return cls(label=data.get("label"), gambar=data.get("gambar"))


class KisahSosial(models.Model):
    kisah_id = models.AutoField(primary_key=True)
    input_text = models.TextField()
    output_text = models.TextField()
    score_human = models.FloatField()
    score_perplexity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    kartu_id = models.ForeignKey(Kartu, on_delete=models.CASCADE)

    def __str__(self):
        return f"Kisah {self.kisah_id}"
