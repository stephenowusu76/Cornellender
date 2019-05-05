//
//  EventDetailViewController.swift
//  Cornellendar
//
//  Created by Sijia Liu on 4/26/19.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//

import Foundation
import UIKit
import MapKit

class EventDetailViewController: UIViewController {
    var event: Event!
    var imageView: UIImageView!
    var nameLabel: UILabel!
    var descriptionTextView: UITextView!
    var dateLabel: UILabel!
    var locationLabel: UILabel!
    var map: MKMapView!
    var dateImageView: UIImageView!
    var locImageView: UIImageView!
    
    let detailViewBig = UIFont(name: "ProductSans-Bold", size: 25)
    let DateLoc = UIFont(name: "SFUIDisplay-Medium", size: 12)
    let Descrpt = UIFont(name: "SFUIDisplay-Regular", size: 15)
    let catLabel = UIFont(name: "ProductSans-Regular", size: 12)
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = event.name
        view.backgroundColor = .white
        
        map = MKMapView.init(frame: CGRect.init(x: 20, y:
            UIScreen.main.bounds.height - 170, width: UIScreen.main.bounds.width - 40, height: UIScreen.main.bounds.height - 500))
        let latitude = Double(event.latitude)
        let longitude = Double(event.longitude)
        let location = CLLocationCoordinate2D(latitude: latitude!, longitude: longitude!)
        let span = MKCoordinateSpan(latitudeDelta: 0.002, longitudeDelta: 0.002)
        let region = MKCoordinateRegion(center: location, span: span)
        let annotation = MKPointAnnotation()
        
        imageView = UIImageView()
        imageView.translatesAutoresizingMaskIntoConstraints = false
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.cornerRadius = 6
        imageView.adjustsImageSizeForAccessibilityContentSizeCategory = true
        view.addSubview(imageView)
        
        nameLabel = UILabel()
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        nameLabel.text = event.name
        nameLabel.textColor = .black
        nameLabel.font = UIFontMetrics.default.scaledFont(for: detailViewBig!)
        nameLabel.numberOfLines = 3
        nameLabel.sizeToFit()
        view.addSubview(nameLabel)
        
        dateImageView = UIImageView()
        dateImageView.image = UIImage(named: "DateImage")
        dateImageView.translatesAutoresizingMaskIntoConstraints = false
        dateImageView.contentMode = .scaleAspectFit
        dateImageView.layer.cornerRadius = 6
        dateImageView.adjustsImageSizeForAccessibilityContentSizeCategory = true
        view.addSubview(dateImageView)
        
        dateLabel = UILabel()
        dateLabel.translatesAutoresizingMaskIntoConstraints = false
        dateLabel.text = event.date
        dateLabel.textColor = .gray
        dateLabel.font = UIFontMetrics.default.scaledFont(for: DateLoc!)
        view.addSubview(dateLabel)
        
        locImageView = UIImageView()
        locImageView.image = UIImage(named: "LocImage")
        locImageView.translatesAutoresizingMaskIntoConstraints = false
        locImageView.contentMode = .scaleAspectFit
        locImageView.layer.cornerRadius = 6
        locImageView.adjustsImageSizeForAccessibilityContentSizeCategory = true
        view.addSubview(locImageView)
        
        locationLabel = UILabel()
        locationLabel.translatesAutoresizingMaskIntoConstraints = false
        locationLabel.text = event.location
        locationLabel.textColor = .gray
        locationLabel.font = UIFontMetrics.default.scaledFont(for: DateLoc!)
        view.addSubview(locationLabel)
        
        descriptionTextView = UITextView()
        descriptionTextView.translatesAutoresizingMaskIntoConstraints = false
        descriptionTextView.text = event.description
        descriptionTextView.textColor = .black
        descriptionTextView.font = UIFontMetrics.default.scaledFont(for: Descrpt!)
        descriptionTextView.isEditable = false
        view.addSubview(descriptionTextView)
        
        map.setRegion(region, animated: true)
        annotation.coordinate = location
        annotation.title = event.location
        map.addAnnotation(annotation)
        view.addSubview(map)
        
        setConstraints()
        getImage(url: event.image)
        
        
    }
    
    func setConstraints() {
        imageView.centerXAnchor.constraint(equalTo: view.centerXAnchor).isActive = true
        imageView.leftAnchor.constraint(equalTo: view.leftAnchor).isActive = true
        imageView.rightAnchor.constraint(equalTo: view.rightAnchor).isActive = true
        imageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor).isActive = true
        
        nameLabel.topAnchor.constraint(equalTo: imageView.bottomAnchor, constant: 6).isActive = true
        nameLabel.leftAnchor.constraint(equalTo: view.leftAnchor, constant: 22).isActive = true
        nameLabel.rightAnchor.constraint(equalTo: view.rightAnchor, constant: -4).isActive = true
        
        dateImageView.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4).isActive = true
        dateImageView.leftAnchor.constraint(equalTo: view.leftAnchor, constant: 22).isActive = true
        dateImageView.rightAnchor.constraint(equalTo: dateImageView.leftAnchor, constant: 15).isActive = true
        dateImageView.heightAnchor.constraint(equalToConstant: 20).isActive = true
        
        dateLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4).isActive = true
        dateLabel.leftAnchor.constraint(equalTo: dateImageView.rightAnchor, constant: 10).isActive = true
        dateLabel.rightAnchor.constraint(equalTo: view.rightAnchor, constant: -22).isActive = true
        dateLabel.heightAnchor.constraint(equalToConstant: 20).isActive = true
        
        locImageView.topAnchor.constraint(equalTo: dateLabel.bottomAnchor, constant: 3).isActive = true
        locImageView.leftAnchor.constraint(equalTo: view.leftAnchor, constant: 22).isActive = true
        locImageView.rightAnchor.constraint(equalTo: locImageView.leftAnchor, constant: 15).isActive = true
        locImageView.heightAnchor.constraint(equalToConstant: 20).isActive = true
        
        locationLabel.topAnchor.constraint(equalTo: dateLabel.bottomAnchor, constant: 3).isActive = true
        locationLabel.leftAnchor.constraint(equalTo: locImageView.rightAnchor, constant: 10).isActive = true
        locationLabel.rightAnchor.constraint(equalTo: view.rightAnchor, constant: -22).isActive = true
        locationLabel.heightAnchor.constraint(equalToConstant: 20).isActive = true
        
        descriptionTextView.topAnchor.constraint(equalTo: locationLabel.bottomAnchor, constant: 4).isActive = true
        descriptionTextView.leftAnchor.constraint(equalTo: view.leftAnchor, constant: 22).isActive = true
        descriptionTextView.rightAnchor.constraint(equalTo: view.rightAnchor, constant: -4).isActive = true
        descriptionTextView.bottomAnchor.constraint(equalTo: map.topAnchor, constant: -5).isActive = true
        
    }
    
    func getImage(url: String) {
        NetworkManager.fetchEventImage(imageURL: url) { (image) in
            DispatchQueue.main.async {
                self.imageView.image = image
            }
        }
    }
}
