//
//  EventCell.swift
//  Cornellendar
//
//  Created by Sijia Liu on 4/26/19.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//

import Foundation
import UIKit

class EventCell: UITableViewCell {
    var eventImageView: UIImageView!
    var eventNameLabel: UILabel!
    var eventDateLabel: UILabel!
    var eventLocationLabel: UILabel!
    var categortyLabel: UILabel!
    var descriptionLabel: UILabel!
    var descriptionTextView: UITextView!
    var categoryLabelWidth: CGFloat = 0.0
    var widthConstraint: NSLayoutConstraint?
    
    let tableCellBig = UIFont(name: "SFUIDisplay-Medium", size: 14)
    let tableCellMed = UIFont(name: "SFUIDisplay-Medium", size: 9)
    let tableCellSmall = UIFont(name: "SFUIDisplay-Regular", size: 9)
    let catLabel = UIFont(name: "ProductSans-Regular", size: 12)
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        eventImageView = UIImageView()
        eventImageView.translatesAutoresizingMaskIntoConstraints = false
        eventImageView.contentMode = .scaleAspectFill
        eventImageView.layer.cornerRadius = 6
        eventImageView.adjustsImageSizeForAccessibilityContentSizeCategory = true
        addSubview(eventImageView)
        
        eventNameLabel = UILabel()
        eventNameLabel.translatesAutoresizingMaskIntoConstraints = false
        eventNameLabel.font = UIFontMetrics.default.scaledFont(for: tableCellBig!)
        eventNameLabel.textColor = .black
        eventNameLabel.numberOfLines = 2
        eventNameLabel.sizeToFit()
        addSubview(eventNameLabel)
        
        eventDateLabel = UILabel()
        eventDateLabel.translatesAutoresizingMaskIntoConstraints = false
        eventDateLabel.font = UIFontMetrics.default.scaledFont(for: tableCellSmall!)
        eventDateLabel.textColor = .black
        eventDateLabel.sizeToFit()
        addSubview(eventDateLabel)
        
        eventLocationLabel = UILabel()
        eventLocationLabel.translatesAutoresizingMaskIntoConstraints = false
        eventLocationLabel.font = UIFontMetrics.default.scaledFont(for: tableCellSmall!)
        eventLocationLabel.textColor = .black
        eventLocationLabel.sizeToFit()
        addSubview(eventLocationLabel)
        
        categortyLabel = UILabel()
        categortyLabel.translatesAutoresizingMaskIntoConstraints = false
        categortyLabel.font = UIFontMetrics.default.scaledFont(for: catLabel!)
        categortyLabel.textColor = .white
        categortyLabel.backgroundColor = .gray
        categortyLabel.layer.masksToBounds = true
        categortyLabel.layer.cornerRadius = categortyLabel.frame.height/2 + 2
        categortyLabel.textAlignment = .center
        addSubview(categortyLabel)
        
        descriptionLabel = UILabel()
        descriptionLabel.translatesAutoresizingMaskIntoConstraints = false
        descriptionLabel.font = UIFontMetrics.default.scaledFont(for: tableCellMed!)
        descriptionLabel.textColor = .gray
        descriptionLabel.numberOfLines = 3
        descriptionLabel.sizeToFit()
        addSubview(descriptionLabel)
        
        setConstraints()
    }
    
    func setConstraints() {
        eventImageView.widthAnchor.constraint(equalToConstant: 154).isActive = true
        eventImageView.heightAnchor.constraint(equalToConstant: 77.5).isActive = true
        eventImageView.centerYAnchor.constraint(equalTo: centerYAnchor).isActive = true
        eventImageView.leftAnchor.constraint(equalTo: leftAnchor, constant: 10).isActive = true
        
        eventNameLabel.leftAnchor.constraint(equalTo: eventImageView.rightAnchor, constant: 20).isActive = true
        eventNameLabel.rightAnchor.constraint(equalTo: rightAnchor, constant: -22).isActive = true
        eventNameLabel.topAnchor.constraint(equalTo: topAnchor, constant: 4).isActive = true
        
        eventDateLabel.leftAnchor.constraint(equalTo: eventImageView.rightAnchor, constant: 20).isActive = true
        eventDateLabel.topAnchor.constraint(equalTo: eventNameLabel.bottomAnchor, constant: 2).isActive = true
        eventDateLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -10).isActive = true
        
        eventLocationLabel.leftAnchor.constraint(equalTo: eventImageView.rightAnchor, constant: 20).isActive = true
        eventLocationLabel.topAnchor.constraint(equalTo: eventDateLabel.bottomAnchor, constant: 1).isActive = true
        eventLocationLabel.widthAnchor.constraint(equalTo: eventDateLabel.widthAnchor).isActive = true
        
        descriptionLabel.leftAnchor.constraint(equalTo: eventImageView.rightAnchor, constant: 20).isActive = true
        descriptionLabel.rightAnchor.constraint(equalTo: rightAnchor, constant: -22).isActive = true
        descriptionLabel.topAnchor.constraint(equalTo: eventLocationLabel.bottomAnchor, constant: 11).isActive = true
        
        NSLayoutConstraint.activate([
            categortyLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -5),
            categortyLabel.heightAnchor.constraint(equalToConstant: 15),
            categortyLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -5)
            ])
    }
    
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func configures(for event: Event) {
        eventNameLabel.text = event.name
        eventDateLabel.text = event.date
        eventLocationLabel.text = event.location
        descriptionLabel.text = event.description
        categortyLabel.text = "# " + event.tag
        getImage(url: event.image)
        
        if let constraint = widthConstraint {
            NSLayoutConstraint.deactivate([
                constraint
            ])
        }
        
        categoryLabelWidth = categortyLabel.text!.getWidth(height: 15, font: categortyLabel.font) + 6
        widthConstraint = categortyLabel.widthAnchor.constraint(equalToConstant: categoryLabelWidth)

        NSLayoutConstraint.activate([
            widthConstraint!
        ])
    }
    
    func getImage(url: String) {
        NetworkManager.fetchEventImage(imageURL: url) { (image) in
            DispatchQueue.main.async {
                self.eventImageView.image = image
            }
        }
    }
    
}

extension String {
    func getWidth(height: CGFloat, font: UIFont) -> CGFloat {
        let constraintRect = CGSize(width: .greatestFiniteMagnitude, height: height)
        let boundingBox = self.boundingRect(with: constraintRect, options: .usesLineFragmentOrigin, attributes: [.font: font], context: nil)
        return ceil(boundingBox.width)
    }
}
