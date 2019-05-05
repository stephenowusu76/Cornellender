//
//  NetworkManager.swift
//  Cornellendar
//
//  Created by Shiman Zhang on 2019/5/4.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//

import Foundation
import Alamofire


class NetworkManager {
    
    private static let endpoint = "http://34.74.152.70/api/events/"
    
    static func getEvents(completion: @escaping ([Event])  -> Void) {
        Alamofire.request(endpoint, method: .get).validate().responseData { (response) in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let eventResponse = try? jsonDecoder.decode(EventDataResponse.self, from: data) {
                    let events = eventResponse.data
                    completion(events)
                } else {
                    print("Invalid response data")
                }
            case .failure(let error):
                print(error.localizedDescription)
            }
        }
    }
    
    static func fetchEventImage(imageURL: String, completion: @escaping (UIImage) -> Void){
        Alamofire.request(imageURL).validate().responseData { (response) in
            switch response.result {
            case .success(let data):
                if let eventImage = UIImage(data: data) {
                    completion(eventImage)
                }
            case .failure(let error):
                print(error.localizedDescription)
            }
        }
    }
}

