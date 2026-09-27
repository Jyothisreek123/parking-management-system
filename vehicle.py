from datetime import datetime




class Vehicle:

  
  def __init__(self,vehicle_number,vehicle_type):
    self.vehicle_number=vehicle_number
    self.vehicle_type=vehicle_type
    self.entry_time=datetime.now()
