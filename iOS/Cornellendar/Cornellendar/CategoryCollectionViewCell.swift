//
//  CategoryCollectionViewCell.swift
//  Cornellendar
//
//  Created by Shiman Zhang on 2019/4/25.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//

import UIKit

class CategoryCollectionViewCell: UICollectionViewCell {
    var categoryLabel: UILabel!
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        
        categoryLabel = UILabel()
        categoryLabel.translatesAutoresizingMaskIntoConstraints = false
        categoryLabel.backgroundColor = .white
        categoryLabel.layer.borderColor = UIColor.black.cgColor
        categoryLabel.layer.borderWidth = 2
        categoryLabel.font = UIFont.systemFont(ofSize: 11)
        categoryLabel.textColor = .black
        categoryLabel.textAlignment = .center
        categoryLabel.layer.masksToBounds = true
        categoryLabel.layer.cornerRadius = categoryLabel.frame.height/2 + 10
        contentView.addSubview(categoryLabel)
        
        setUpConstraint()
    }
    
    func setUpConstraint() {
        NSLayoutConstraint.activate([
            categoryLabel.topAnchor.constraint(equalTo: contentView.topAnchor),
            categoryLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            categoryLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor),
            categoryLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor)
            ])
    }

    func configure(category: Category) {
        categoryLabel.text = stringFromCategory(category)
    }
    
    func toggleColor(for selected: Bool) {
        if selected {
            categoryLabel.backgroundColor = .gray
            categoryLabel.layer.borderColor = UIColor.gray.cgColor
            categoryLabel.textColor = .white
        } else {
            categoryLabel.backgroundColor = .white
            categoryLabel.layer.borderColor = UIColor.black.cgColor
            categoryLabel.textColor = .black
        }
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
