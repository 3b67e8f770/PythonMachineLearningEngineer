variable "location" {
  description = "Region w Azure, gdzie powstaną zasoby"
  type        = string
  default     = "West Europe" # Np. serwery w Holandii
}

variable "project_prefix" {
  description = "Przedrostek dla naszych zasobów, żeby łatwo je znaleźć"
  type        = string
  default     = "lossprev" # Od Loss Prevention
}