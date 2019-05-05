//
//  ViewController.swift
//  Cornellendar
//
//  Created by Shiman Zhang on 2019/4/25.
//  Copyright © 2019 Shiman Zhang, Sijia Liu. All rights reserved.
//
import UIKit

class ViewController: UIViewController {
    var filterCollectionView: UICollectionView!
    var eventTableView: UITableView!
    
    var categoryList: [Category]!
    var events: [Event] = [Event]()
    var activeFilter: Set<Category> = []
    var filteredEvents: [Event]! = []
    var displayedEvents: [Event] = []
    var filterSelected: Dictionary<Category, Bool> = [:]
    
    let spacing: CGFloat = 8
    let filterViewHeight: CGFloat = 40
    let filterReuseIdentifier: String = "Category"
    let eventReuseIdentifier: String = "Event"
    let searchInput = UISearchController(searchResultsController: nil)
    
    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = .white
        title = "Cornellendar"
        navigationController?.navigationBar.barTintColor = UIColor(red: 1.0, green: 0.871, blue: 0.012, alpha: 1.0)
        navigationController?.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont.systemFont(ofSize: 25, weight: .bold), .foregroundColor: UIColor.white]
    
        categoryList = [.academic, .movies, .music, .social, .sports, .seminar]
        
        for category in categoryList {
            filterSelected[category] = false
        }
        
        createEvents()

        let filterLayout = UICollectionViewFlowLayout()
        filterLayout.minimumInteritemSpacing = spacing
        filterLayout.minimumLineSpacing = spacing
        filterLayout.scrollDirection = .horizontal
        
        filterCollectionView = UICollectionView(frame: .zero, collectionViewLayout: filterLayout)
        filterCollectionView.translatesAutoresizingMaskIntoConstraints = false
        filterCollectionView.backgroundColor = .white
        filterCollectionView.dataSource = self
        filterCollectionView.delegate = self
        filterCollectionView.register(CategoryCollectionViewCell.self, forCellWithReuseIdentifier: filterReuseIdentifier)
        view.addSubview(filterCollectionView)
        
        
        // Set up Tableview
        eventTableView = UITableView()
        eventTableView.translatesAutoresizingMaskIntoConstraints = false
        eventTableView.register(EventCell.self, forCellReuseIdentifier: eventReuseIdentifier)
        eventTableView.backgroundColor = .white
        eventTableView.separatorStyle = .none
        eventTableView.delegate = self
        eventTableView.dataSource = self
        view.addSubview(eventTableView)
        
        
        searchInput.searchResultsUpdater = self
        searchInput.obscuresBackgroundDuringPresentation = false
        searchInput.searchBar.placeholder = "Search for Events!"
        navigationItem.searchController = searchInput
        navigationItem.hidesSearchBarWhenScrolling = false
        definesPresentationContext = true
        
        
        setUpConstraits()
    }
    
    func setUpConstraits() {
        NSLayoutConstraint.activate([
            filterCollectionView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            filterCollectionView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 5),
            filterCollectionView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -5),
            filterCollectionView.heightAnchor.constraint(equalToConstant: filterViewHeight),
            
            eventTableView.topAnchor.constraint(equalTo: filterCollectionView.bottomAnchor, constant: 5),
            eventTableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            eventTableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            eventTableView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
            
            ])
    }
    
    func createEvents() {
        NetworkManager.getEvents { events in
            self.events = events
            self.filteredEvents = events
            self.displayedEvents = events
            DispatchQueue.main.async {
                self.eventTableView.reloadData()
            }
        }
    }
}

extension ViewController: UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return categoryList.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: filterReuseIdentifier, for: indexPath) as! CategoryCollectionViewCell
        cell.configure(category: categoryList[indexPath.item])
        cell.toggleColor(for: filterSelected[categoryList[indexPath.item]]!)
        return cell
    }
}

extension ViewController: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let selected = categoryList[indexPath.item]
        if filterSelected[selected] == false {
            changeFilter(filter: selected, remove: false)
            filterSelected.updateValue(true, forKey: selected)
        } else {
            changeFilter(filter: selected, remove: true)
            filterSelected.updateValue(false, forKey: selected)
        }
        filterEvents()
        updateSearchResults(for: searchInput)
        filterCollectionView.reloadData()
    }
    
    // helper function: add or remove the selected filter
    func changeFilter(filter: Category, remove: Bool) {
        if remove {
            activeFilter.remove(filter)
        } else {
            activeFilter.insert(filter)
        }
    }
}

extension ViewController: UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let height = collectionView.frame.height - 15
        let width = (collectionView.frame.width - 4 * spacing) / 5
        return CGSize(width: width, height: height)
    }
}

extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        let height = tableView.frame.height / 4
        return height
    }
}

extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return displayedEvents.count
    }
    
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: eventReuseIdentifier, for: indexPath) as! EventCell
        cell.backgroundColor = .white
        let event = displayedEvents[indexPath.row]
        cell.configures(for: event)
        return cell
    }
    
    //display eventDetailViewController
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let event = displayedEvents[indexPath.row]
        let detailVC = EventDetailViewController()
        detailVC.event = event
        self.navigationController?.pushViewController(detailVC, animated: true)
    }
    
    func filterEvents() {
        if activeFilter.count == 0 {
            filteredEvents = events
        } else {
            var newFilteredEvents: [Event] = []
            for event in events {
                if eventInActiveFilter(for: event) {
                    newFilteredEvents.append(event)
                }
            }
            filteredEvents = newFilteredEvents
        }
    }
    // helper method for filterEvents()
    // returns true if the category of the event matches one of the categories in active Filter set
    func eventInActiveFilter(for event: Event) -> Bool {
        for category in activeFilter {
            let string = stringFromCategory(category)
            if event.tag == string {
                return true
            }
        }
        return false
    }
    
}

extension ViewController: UISearchResultsUpdating {
    func updateSearchResults(for searchController: UISearchController) {
        if let searchText = searchController.searchBar.text, !searchIsEmpty() {
            var newEvents: [Event] = []
            for event in filteredEvents {
                if textInName(for: searchText, event: event) {
                    newEvents.append(event)
                }
            }
            displayedEvents = newEvents
        } else {
            displayedEvents = filteredEvents
        }
        eventTableView.reloadData()
    }
    
    func textInName(for searchText: String, event: Event) -> Bool {
        return event.name.lowercased().contains(searchText.lowercased())
    }
    
    func searchIsEmpty() -> Bool {
        return searchInput.searchBar.text?.isEmpty ?? true
    }
    
}


func stringFromCategory(_ category: Category) -> String {
    switch category {
    case .academic:
        return "Academic"
    case .movies:
        return "Movies"
    case .music:
        return "Music"
    case .social:
        return "Social"
    case .sports:
        return "Sports"
    case .seminar:
        return "Seminar"
    }
}


