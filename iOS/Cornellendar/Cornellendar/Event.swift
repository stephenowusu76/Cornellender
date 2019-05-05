//
//  Event.swift
//  Cornellendar
//
//  Created by Shiman Zhang on 2019/4/25.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//

import Foundation
import UIKit
import MapKit

enum Category {
    case social
    case music
    case movies
    case academic
    case sports
    case seminar
}

enum Month {
    case jan
    case feb
    case mar
    case apr
    case may
    case jun
    case jul
    case aug
    case sep
    case oct
    case nov
    case dec
}

struct Event: Codable {
    var id: Int
    var date: String
    var name: String
    var description: String
    var longitude: String
    var latitude: String
    var location: String
    var tag: String
    var image: String
    var link: String
    
    func stringFromMonth(month: Month) -> String {
        switch month {
        case .jan:
            return "Jan. "
        case .feb:
            return "Feb. "
        case .mar:
            return "Mar. "
        case .apr:
            return "Apr. "
        case .may:
            return "May. "
        case .jun:
            return "Jun. "
        case .jul:
            return "Jul. "
        case .aug:
            return "Aug. "
        case .sep:
            return "Sep. "
        case .oct:
            return "Oct. "
        case .nov:
            return "Nov. "
        case .dec:
            return "Dec. "
        }
    }
}

struct EventDataResponse: Codable {
    var data: [Event]
}
