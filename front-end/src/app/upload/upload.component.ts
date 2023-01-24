import { Component, OnInit, HostListener, OnDestroy } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UploaderService } from '../services/uploader.service'
@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  probableImages: Array<any> = [];
  progress: number;
  infoMessage: any;
  isUploading: boolean = false;
  file: File;

  imageUrl: string | ArrayBuffer =
    "https://bulma.io/images/placeholders/128x128.png";
  fileName: string = "عکسی انتخاب نشده است";

  @HostListener('window:beforeunload') removeLocalStorage() {
    localStorage.removeItem("probableImages");
  }

  constructor(private toastr: ToastrService, private uploader: UploaderService) { }

  ngOnInit() {
    let data = localStorage.getItem("probableImages");
    if (data) {
      this.probableImages = JSON.parse(data);
    }
  }

  onChange(file: File) {
    if (file) {
      this.fileName = file.name;
      this.file = file;

      const reader = new FileReader();
      reader.readAsDataURL(file);

      reader.onload = event => {
        this.imageUrl = reader.result;
      };
    }
  }

  onUpload() {
    console.log("Image uploaded")
    this.infoMessage = null;
    this.progress = 0;
    this.isUploading = true;

    this.uploader.upload(this.file).subscribe(message => {
      this.isUploading = false;
      console.log("Injast")
      console.log(message)
      this.probableImages = message;
      // DOTO: Disable for presentation.
      localStorage.setItem("probableImages", JSON.stringify(this.probableImages))
    });
  }

}
