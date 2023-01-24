import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { DetailComponent } from './detail/detail.component';
import { GalleryComponent } from './gallery/gallery.component';
import { AboutComponent } from './about/about.component';

const routes: Routes = [
  { path: 'upload', component: UploadComponent },

  { path: 'detail/:id', component: DetailComponent },

  { path: 'gallery', component: GalleryComponent },

  { path: 'about', component: AboutComponent },

  // Otherwise redirect to home
  { path: '**', redirectTo: '/upload', pathMatch: 'full' }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
