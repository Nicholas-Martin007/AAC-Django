from django.db import models


class Kartu(models.Model):
    kartu_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)
    gambar = models.TextField()
    kategori = models.TextField(default="default")
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def to_json(self):
        return {
            "kartu_id": self.kartu_id,
            "label": self.label,
            "gambar": self.gambar,
            "kategori": self.kategori,
            "flag": self.flag,
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            label=data.get("label"),
            gambar=data.get("gambar"),
            kategori=data.get("kategori", "default"),
            flag=data.get("flag", False),
        )


class KisahSosial(models.Model):
    kisah_id = models.AutoField(primary_key=True)
    input_text = models.TextField()
    output_text = models.TextField()
    score_human = models.FloatField()
    score_perplexity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    kartu = models.ManyToManyField("Kartu", through="KartuKisah")

    def __str__(self):
        return f"Kisah {self.kisah_id}"


class KartuKisah(models.Model):
    kartu = models.ForeignKey(Kartu, on_delete=models.CASCADE)
    kisah = models.ForeignKey(KisahSosial, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = ("kartu", "kisah")
